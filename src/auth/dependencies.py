from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from fastapi import Request, status, Depends
from sqlmodel import select
from typing import List, Any

from .models import User
from .utils import decode_token
from src.db.redis import jti_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.services import UserService

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        credentials = creds.credentials

        token_data = decode_token(credentials)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Invalid or expired access token",
                    "resolution": "Please get a new token",
                },
            )

        if await jti_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Token is invalid or has been revoked",
                    "resolution": "Please get a new token",
                },
            )

        # Looks for the function 'verify_token' among the child classes (AccessTokenBearer & RefreshTokenBearer) first,
        # if not found falls-back to parent class 'verify_token'
        self.verify_token(token_data)

        return token_data

    def verify_token(self, token_data: dict):
        raise NotImplementedError("Please Override this method in clild classes")


class AccessTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict):
        # Since token_data can be None, so "token['refresh']", 'NoneType' object is not subscriptable , so we can use "token.get('refresh')"
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict):
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Refresh token"
            )


# dependecy for the "/me" route
async def get_current_user(
    token_data: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_data["user"]["email"]

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:

        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: User = Depends(get_current_user)) -> Any:

        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perfom this action",
        )
