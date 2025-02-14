from ninja import Schema, ModelSchema
from django.contrib.auth import get_user_model
from typing import List

UserModel = get_user_model()


class UserLoginSchema(Schema):
    email: str
    password: str


class CreateUserSchema(Schema):
    email: str
    password: str
    first_name: str
    last_name: str


class UserSchema(ModelSchema):
    class Meta:
        model = UserModel
        exclude = ["password", "last_login", "user_permissions"]


class ChangePasswordSchema(Schema):
    password: str
    email: str


class UpdateUserSchema(Schema):
    first_name: str | None = None
    last_name: str | None = None
    is_verified: bool | None = None
    phone_number: str | None = None


class PasswordChangedResponseSchema(Schema):
    message: str


class LoginResponseSchema(Schema):
    access_token: str
    user_id: int | str


UsersListSchema = List[UserSchema]
