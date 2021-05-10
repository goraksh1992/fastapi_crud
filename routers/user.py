from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from hashing import Hashing
from database import get_db 

router = APIRouter(
    tags=['Users']
)

@router.post('/users')
def add_user(userData: schemas.User, db: Session = Depends(get_db)):
    user = models.User(name=userData.name, email=userData.email, 
        password=Hashing.bcrypt_password(userData.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/users', response_model=List[schemas.ShowUsers])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="No users found")
    return users


@router.get('/users/{id}', response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="No user found")
    return user