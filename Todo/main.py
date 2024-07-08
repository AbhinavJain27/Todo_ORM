from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Annotated
import models
from database import SessionLocal,engine
from sqlalchemy.orm import Session

app=FastAPI()
models.base.metadata.create_all(bind=engine)

class Post_Base(BaseModel):
    title:str
    content:str
    user_id:int

class UserBase(BaseModel):
    username:str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@app.post("/post/",status_code=status.HTTP_201_CREATED)
async def create_post(post:Post_Base,db:db_dependency):
    db_post=models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.delete("/post/{post_id}",status_code=status.HTTP_202_ACCEPTED)
async def delete_post(post_id:int,db:db_dependency):
    db_post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404,details='Post was not found')
    db.delete(db_post)
    db.commit()

@app.post("/users/",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase,db:db_dependency):
    db_user=models.User(**user.dict())
    db.add(db_user)
    db.commit()
    user=db.query(models.User).filter(models.User.username==user.username).first()
    id=user.user_id
    return f"User with username {user.username} was created with id = {id}"

@app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
async def get_user(user_id:int , db:db_dependency):
    user=db.query(models.User).filter(models.User.user_id== user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found") 
    return user