from database import base
from sqlalchemy import Boolean, Column,Integer, String

class User(base):
    __tablename__='users'

    user_id=Column(Integer,primary_key=True , index=True)
    username=Column(String(50),unique=True)

class Post(base):
    __tablename__='posts'

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(50))
    content=Column(String(100))
    user_id=Column(Integer)