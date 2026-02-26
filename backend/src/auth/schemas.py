from typing import Optional

from pydantic import BaseModel

from backend.src.appstatus.schemas import AppStatus
from backend.src.users.schemas import UserSelf

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str

class LoginResponse(BaseModel):
    app_status: AppStatus
    access_token: AccessToken
    refresh_token: Optional[RefreshToken] = None
    user: UserSelf

class AccessTokenData(BaseModel):
    user_id: int
    username: str
    language: str

class RefreshTokenData(BaseModel):
    user_id: int

class LoginRefreshTokenPost(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken

class GoogleTokenData(BaseModel):
    email: str
    email_verified: bool
    sub: str
    hd: Optional[str] = None

class AppleTokenData(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: str

class AppleIdTokenData(BaseModel):
    email: str
    sub: str
