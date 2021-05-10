from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str

class Blogs(Blog):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUsers(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUser(ShowUsers):

    # This will give you all blog added by user
    blogs: List[Blogs] = []

    class Config:
        orm_mode = True


class Users(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
        

# Get blog with creator
class ShowBlog(BaseModel):
    title: str
    body: str

    creator: Users

    class Config:
        orm_mode = True