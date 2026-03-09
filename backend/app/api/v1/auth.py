from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.deps import get_auth_service
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str =Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128) 


class RegisterResponse(BaseModel):
    id: int
    username: str


@router.post("/register", summary="Register user", response_model=RegisterResponse, status_code=201)
def register(
    payload: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> RegisterResponse:
    user = auth_service.register_user(username=payload.username, password=payload.password)
    return RegisterResponse(**user)