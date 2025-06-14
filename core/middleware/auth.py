from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.utils.aes import AESCipher
from models.user import User

ACCESS_TOKEN_EXPIRE_MINUTES = 5

class JWTTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        access_token = request.cookies.get("accessToken")
        refresh_token = request.cookies.get("refreshToken")
        
        # If no access token but have refresh token, try to create new access token
        if not access_token and refresh_token:
            token = AESCipher(refresh_token)
            if token.is_valid:
                # Create new access token
                access_token = self.create_access_token(ACCESS_TOKEN_EXPIRE_MINUTES, token.json)
                # Set user in request state
                request.state.user = User(**token.json)
                response = await call_next(request)
                response.set_cookie(
                    key="accessToken",
                    value=access_token,
                    httponly=True,
                    max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
                return response
        
        if access_token:
            token = AESCipher(token=access_token)
            if token.is_valid:
                # Set user in request state
                request.state.user = User(**token.json)
                return await call_next(request)

        request.state.user = None
        response = await call_next(request)
        return response

    def create_access_token(self, expires_delta: int, user_data: dict = None) -> str:
        token_object = AESCipher().generate_token(
            expires_in=expires_delta,
            data=user_data
        )
        return token_object.token