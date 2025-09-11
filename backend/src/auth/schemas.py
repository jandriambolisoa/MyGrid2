from pydantic import BaseModel

from backend.src.users.schemas import UserSelf

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str

class LoginResponse(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken
    user: UserSelf

class AccessTokenData(BaseModel):
    username: str
    language: str

class RefreshTokenData(BaseModel):
    user_id: int

class LoginRefreshTokenPost(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken
