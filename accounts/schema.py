from ninja import Schema, ModelSchema, Field, FilterSchema
from django.contrib.auth import get_user_model
from typing import List, Optional


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


class UsersFilterSchema(FilterSchema):
    email: Optional[str] = None
    is_verified: Optional[bool] = None
    first_name: Optional[str] = Field(None, q="first_name__icontains")
    last_name: Optional[str] = Field(None, q="last_name__icontains")
