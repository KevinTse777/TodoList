from fastapi import FastAPI
from app.api.v1.system import router as system_router
from app.api.v1.todos import router as todos_router
from app.core.exceptions import register_exception_handlers

app = FastAPI(title="Todo API", version="0.1.0")
register_exception_handlers(app)
app.include_router(system_router)
app.include_router(todos_router)
