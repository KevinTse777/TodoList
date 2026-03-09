from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    #业务错误码，先用字符串，后续枚举
    code: str
    #给前端展示错误信息
    message: str
    #保留原始细节
    details: object | None = None


class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: object | None = None
    ) -> None :
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # 统一处理422参数校验
        payload = ErrorResponse(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=exc.errors(),
        )
        return JSONResponse(status_code=422, content=payload.model_dump())
    
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
        payload = ErrorResponse(
            code=exc.code,
            message=exc.message,
            details=exc.details,
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())
    

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        #兜底异常
        payload = ErrorResponse(
            code="INTERNAL_SERVER_ERROR",
            message="Internal server error",
            details=None,
        )
        return JSONResponse(status_code=500, content=payload.model_dump())
    

