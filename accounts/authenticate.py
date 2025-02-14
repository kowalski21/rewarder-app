from django.contrib.auth import get_user_model
from ninja.errors import AuthenticationError
import jwt
from munch import Munch
from django.conf import settings
import pendulum

UserModel = get_user_model()


def check_user_exists(email: str) -> UserModel | None:
    try:
        user = UserModel.objects.get(email=email)
        return user
    except UserModel.DoesNotExist:
        return None


def get_user_from_db(email: str) -> UserModel | None:
    try:
        user = UserModel.objects.get(email=email)
        return user
    except UserModel.DoesNotExist:
        raise AuthenticationError("Invalid User Credentials")


def generate_jwt_token(
    payload: dict,
    secret_key: str,
    expires_in_minutes: int = 60,
    algorithm: str = "HS256",
) -> str:
    now = pendulum.now()
    token_payload = Munch(
        iat=now.int_timestamp, exp=now.add(minutes=expires_in_minutes).int_timestamp
    )
    token_payload.update(payload)
    token = jwt.encode(payload=token_payload, key=secret_key, algorithm=algorithm)
    return token


def authenticate_user(email: str, password: str) -> dict:
    user = get_user_from_db(email)
    if not user.check_password(password):
        raise AuthenticationError("Invalid User Credentials")
    jwt_payload = Munch(user_id=user.id)
    token = generate_jwt_token(
        jwt_payload,
        secret_key=settings.JWT_SECRET_KEY,
        expires_in_minutes=settings.JWT_ACCESS_TTL,
    )
    return Munch(access_token=token, user_id=user.id)


def verify_jwt_token(
    token: str, secret_key: str, algorithms: list[str] = ["HS256"]
) -> dict:
    try:
        payload = jwt.decode(jwt=token, key=secret_key, algorithms=algorithms)
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token Expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid Token")
