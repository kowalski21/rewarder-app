from ninja import Router
from .schema import UserLoginSchema,LoginResponseSchema

router = Router


@router.post("/login")
def auth_login(request,payload:UserLoginSchema):
    # Find user by email
    # Check Password
    # Generate JWT token