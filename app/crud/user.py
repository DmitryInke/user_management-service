from sqlalchemy.orm import Session
from app.db.models import User


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def save_user(db: Session, user: User) -> None:
    db.add(user)
    db.commit()
    db.refresh(user)
