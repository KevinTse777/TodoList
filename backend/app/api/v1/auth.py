from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.deps import get_auth_service
from app.services.auth_service import AuthService
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import get_auth_service, get_current_user
from app.models.user import User




router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    # 注册入参
    username: str =Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128) 


class RegisterResponse(BaseModel):
    id: int
    username: str


class LoginRequest(BaseModel):
    # 当前是 JSON登陆
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeResponse(BaseModel):
    id: int
    username: str

@router.post("/register", summary="Register user", response_model=RegisterResponse, status_code=201)
def register(
    payload: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> RegisterResponse:
    user = auth_service.register_user(username=payload.username, password=payload.password)
    return RegisterResponse(**user)


@router.post("/login", summary="User login", response_model=TokenResponse)
def login(
    # OAuth2 密码模式：用户名/密码从 x-www-form-urlencoded 读取
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    # 认证成功后签发 JWT
    user = auth_service.authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    token = create_access_token(subject=user["username"])
    return TokenResponse(access_token=token)


@router.get("/me", summary="Get current user", response_model=MeResponse)
def get_me(
    # 依赖层负责解析 Bearer Token 并查处用户
    current_user: User = Depends(get_current_user),
) -> MeResponse:
    return MeResponse(id=current_user.id, username=current_user.username)

