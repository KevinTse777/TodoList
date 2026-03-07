from typing import Optional

from app.repositories.todo_repository import TodoRepository
class TodoService:
    def __init__(self, repo: TodoRepository) -> None:
        self.repo = repo
    
    # service 层承接业务逻辑；后续这里会接数据库 repository
    def list_todos(self, limit: int, offset: int, done: Optional[bool]) -> list[dict]:
        todos = self.repo.list_todos(limit=limit, offset=offset, done=done)

        return [{"id": t.id, "title": t.title, "done": t.done} for t in todos]