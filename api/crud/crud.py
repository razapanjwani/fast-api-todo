from sqlalchemy.orm import Session
from sqlalchemy import select
from ..model.model import *
from fastapi import HTTPException
from ..auth.service import get_current_user
class TodoCrud:

    def crud_get_todo(self,db:Session,user):
        todos = db.query(Todo).filter(Todo.user_id == user.id).all()
        return todos

    
    def crud_create_todo(self,todo_data,db:Session,user):

        todo = Todo(title = todo_data.title, description = todo_data.description,user_id = user.id)
        # user = db.query(model.User).filter(model.User.id == todo_data.user_id).first()
        # user.todos.append(todo)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def crud_update_todo(self,todo_id,updated_todo,db):
        todo = db.query(Todo).filter(todo_id == Todo.id).first()
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.title = updated_todo.title
        todo.description = updated_todo.description
        db.commit()
        return todo

    def crud_delete_todo(self,todo_id,db):
        deleted_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if deleted_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        db.delete(deleted_todo)
        db.commit()
        return {"message":"Todo deleted"}

class UserCrud:
    def get_user_by_email(self,user_email,db):
        return db.query(User).filter(User.email == user_email).first()
    
    def crud_get_user(self,db:Session):
        return db.query(User).all()
        

    
