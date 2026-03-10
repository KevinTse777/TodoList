from typing import Optional

from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel, Field, ConfigDict
from app.services.todo_service import TodoService
from app.api.deps import get_todo_service, get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/todos", tags=["todo"])

class TodoItem(BaseModel):
    id: int
    title:str = Field(min_length=1, max_length=120)
    done: bool

class TodoListResponse(BaseModel):
    # 列表接口统一返回 items + 分页信息
    items: list[TodoItem]
    limit: int
    offset: int
    total: int

class TodoCreate(BaseModel):
    #创建请求体
    title: str = Field(min_length=1, max_length=120)


class TodoCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    done: bool

@router.post("", summary="Create todo", response_model=TodoCreateResponse, status_code=201)
def create_todo(
    payload: TodoCreate,
    service: TodoService = Depends(get_todo_service),
    # 依赖注入了拿到当前登录用户
    current_user: User = Depends(get_current_user),
) -> TodoCreateResponse:
    row = service.create_todo(title=payload.title, owner_id=current_user.id)
    return TodoCreateResponse(**row)

@router.get("", summary="List todos", response_model=TodoListResponse)
def list_todos(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    done: Optional[bool] = Query(default=None),
    service: TodoService = Depends(get_todo_service),
    # 所有查询都按当前用户隔离
    current_user: User = Depends(get_current_user)    
) -> TodoListResponse:
    # 路由层只处理HTTP参数与响应组装，业务逻辑交给service
    # 只查询当前用户的todo
    rows = service.list_todos(limit=limit, offset=offset, done=done, owner_id=current_user.id)
    items = [TodoItem(**row) for row in rows]
    return TodoListResponse(items=items, limit=limit, offset=offset, total=len(items))