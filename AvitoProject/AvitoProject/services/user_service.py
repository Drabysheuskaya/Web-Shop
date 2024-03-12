from sqlalchemy.orm import Session
from database import crud
from database.models import User
from database.shemas import UserRequest


def create_user(db: Session, user_request: UserRequest):
    user = db.query(User).filter(User.email == user_request.email).first()
    if user is not None:
        return "User with such email already exist"
    crud.create_user(db, user_request)
    return "Create successfully"
