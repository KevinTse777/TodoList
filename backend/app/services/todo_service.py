from typing import Optional

from app.repositories.todo_repository import TodoRepository
class TodoService:
    def __init__(self, repo: TodoRepository) -> None:
        self.repo = repo
    
    # service 层承接业务逻辑；后续这里会接数据库 repository
    def list_todos(self, limit: int, offset: int, done: Optional[bool], owner_id: int) -> list[dict]:
        todos = self.repo.list_todos(limit=limit, offset=offset, done=done, owner_id=owner_id)

        return [{"id": t.id, "title": t.title, "done": t.done} for t in todos]
    
    def create_todo(self, title: str, owner_id: int) -> dict:
        todo = self.repo.create_todo(title=title,owner_id=owner_id)
        return {"id": todo.id, "title": todo.title, "done": todo.done}
    
    def update_todo_done(self, todo_id: int, owner_id: int, done: bool) -> dict | None:
        todo = self.repo.update_done(todo_id = todo_id, owner_id=owner_id, done=done)
        if todo is None:
            return None
        return{"id": todo.id, "title": todo.title, "done": todo.done}
    