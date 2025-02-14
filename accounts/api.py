from ninja import Router, Query
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate, PageNumberPagination
from django.contrib.auth import get_user_model, get_user
from accounts.models import AccountUser
from .schema import (
    UserLoginSchema,
    LoginResponseSchema,
    ChangePasswordSchema,
    CreateUserSchema,
    UserSchema,
    PasswordChangedResponseSchema,
    UpdateUserSchema,
    UsersListSchema,
    UsersFilterSchema,
)
from .authenticate import (
    authenticate_user,
    get_user_from_db,
    check_user_exists,
    AuthenticationBearer,
)
from .utils import generate_username
from ninja.errors import ValidationError, HttpError

router = Router()

UserModel = get_user_model()


@router.post("/login", response=LoginResponseSchema)
def auth_login(request, payload: UserLoginSchema):
    user_payload = authenticate_user(email=payload.email, password=payload.password)
    return user_payload


@router.post("/change-password", response=PasswordChangedResponseSchema)
def change_user_password(request, payload: ChangePasswordSchema):
    user = check_user_exists(email=payload.email)
    if user:
        user.set_password(payload.password)
        user.save()
        return {"message": "Password changed"}
    raise HttpError(404, "User not found")


@router.get("/me", response=UserSchema, auth=AuthenticationBearer())
def current_user(request):
    return request.auth


@router.get("/{user_id}", response=UserSchema)
def retrieve_user(request, user_id: int):
    user = get_object_or_404(UserModel, id=user_id)
    return user


@router.patch("/{user_id}", response=UserSchema)
def update_user(request, user_id: int, payload: UpdateUserSchema):
    user = get_object_or_404(UserModel, id=user_id)
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    return user


@router.post("/", response=UserSchema)
def register_user(request, payload: CreateUserSchema):
    user_payload = payload.model_dump()
    password = user_payload.pop("password")
    user = check_user_exists(payload.email)
    if user:
        raise ValidationError("User Already exists")
    try:
        new_user = AccountUser.objects.create(
            **user_payload, username=generate_username()
        )
        new_user.set_password(password)
        new_user.save()
        return new_user
    except Exception as e:
        raise ValidationError(str(e))


@router.get("/", response=UsersListSchema)
@paginate(PageNumberPagination)
def list_users(request, filters: UsersFilterSchema = Query(...)):
    users = UserModel.objects.all()
    users = filters.filter(users)

    return users
