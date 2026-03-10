from fastapi import FastAPI
from app.api.v1.system import router as system_router
from app.api.v1.todos import router as todos_router
from app.api.v1.auth import router as auth_router
from app.core.exceptions import register_exception_handlers
from app.middlewares.request_logging import request_logging_middleware


app = FastAPI(title="Todo API", version="0.1.0")
register_exception_handlers(app)
app.include_router(system_router)
app.include_router(todos_router)
app.include_router(auth_router)
# 全局请求日志中间件：记录 request_id/路径/状态码/耗时
app.middleware("http")(request_logging_middleware)

