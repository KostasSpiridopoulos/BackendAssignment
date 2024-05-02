from pydantic import BaseModel
from typing import List
from datetime import date

class AuthorCreate(BaseModel):
    name: str

class TagCreate(BaseModel):
    name: str

class AuthorCreate(BaseModel):
    name: str

class TagCreate(BaseModel):
    name: str

class ArticleCreate(BaseModel):
    title: str
    abstract: str
    publication_date: date
    authors: List[int]
    tags: List[int]

class ArticleUpdate(BaseModel):
    article_id: int
    title: str
    abstract: str
    publication_date: date
    authors: List[int]
    tags: List[int]

class ArticleDelete(BaseModel):
    article_id: int

class CommentCreate(BaseModel):
    article_id: int
    content: str

class CommentGet(BaseModel):
    article_id: int

class CommentDelete(BaseModel):
    comment_id: int

class CommentUpdate(BaseModel):
    comment_id: int
    content: str
    
class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str