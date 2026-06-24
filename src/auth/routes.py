from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime

from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBookModel
from .services import UserService
from src.db.main import get_session
from .utils import create_access_token, decode_token, verify_passwd
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_Account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exist = await user_service.get_user_by_email(email, session)  # a bool

    # check if an user with that email already exists
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_user(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password

    # fetch user from db
    user = await user_service.get_user_by_email(email, session)

    # If user exists
    if user is not None:
        # Verify password
        password_valid = verify_passwd(password, user.password_hash)

        # If password is valid
        if password_valid:
            # Create an Access token
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
            )

            # Create a Refresh token
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            # Return our Token
            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "user_uid": str(user.uid),
                    },  # didnt add role = user.role here
                }
            )

    # If password verification fails
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email or Password"
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_data: dict = Depends(RefreshTokenBearer())):

    expiry_timestamp = token_data["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_data["user"])

        return JSONResponse({"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
    )


# To show user their details
@auth_router.get("/me", response_model=UserBookModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


# we need to revoke the access token when someone logs out
@auth_router.get("/logout")
async def revoke_token(token_data: dict = Depends(AccessTokenBearer())):
    jti = token_data["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK
    )
