from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.security import hash_password
from app.schemas.user import UserLogin
from app.auth.security import verify_password
from app.auth.jwt_handler import create_access_token

from app.auth.role_checker import verify_role

router = APIRouter()

@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }


@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {"error": "Invalid email"}

    if not verify_password(
        user.password,
        db_user.password
    ):
        return {"error": "Invalid password"}

    access_token = create_access_token(
        data={
            "user_id": db_user.id,
            "email": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/manager-only")
def manager_route(
    user=Depends(verify_role("manager"))
):
    return {
        "message": "Welcome Manager"
    }