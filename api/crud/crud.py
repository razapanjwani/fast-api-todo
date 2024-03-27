from sqlmodel import Session,select
from ..model.model import *
from fastapi import HTTPException
from ..auth.service import get_current_user
class TodoCrud:

    def crud_get_todo(self,db:Session,user):
        # todos = db.query(Todo).filter(Todo.user_id == user.id).all()
        todos = db.exec(select(Todo).where(Todo.user_id == user.id)).all()
        return todos

    
    def crud_create_todo(self,todo_data,db:Session,user):

        todo = Todo(title = todo_data.title, description = todo_data.description,user_id = user.id)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def crud_update_todo(self,todo_id,updated_todo,db:Session):
        todo = db.exec(select(Todo).where(todo_id == Todo.id)).first()
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.title = updated_todo.title
        todo.description = updated_todo.description
        db.commit()
        return todo

    def crud_delete_todo(self,todo_id,db:Session):
        deleted_todo = db.exec(select(Todo).where(Todo.id == todo_id)).first()
        if deleted_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        db.delete(deleted_todo)
        db.commit()
        return {"message":"Todo deleted"}


        

    
