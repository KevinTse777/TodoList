from typing import Optional


class TodoService:
    # service 层承接业务逻辑；后续这里会接数据库 repository
    def list_todos(self, limit: int, offset: int, done: Optional[bool]) -> list[dict]:
        fake_data =[
            {"id": 1,"title": "Learn FastAPI basics", "done": False},
            {"id": 2, "title": "Build Todo API", "done": True},
        ]
        if done is not None:
            fake_data = [item for item in fake_data if["done"] == done]
        return fake_data[offset : offset + limit]