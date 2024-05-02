from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date

class UserArticleLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)

class UserCommentLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    comment_id: Optional[int] = Field(default=None, foreign_key="comment.id", primary_key=True)

class User(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(default=None, unique=True)
    hashed_password: str
    articles: List["Article"] = Relationship(back_populates="user", link_model=UserArticleLink)
    comments: List["Comment"] = Relationship(back_populates="user", link_model=UserCommentLink)

class ArticleAuthorLink(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)
    author_id: Optional[int] = Field(default=None, foreign_key="author.id", primary_key=True)

class ArticleTagLink(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class ArticleCommentLink(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)
    comment_id: Optional[int] = Field(default=None, foreign_key="comment.id", primary_key=True)

class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    abstract: str
    publication_date: Optional[date]
    user: User = Relationship(back_populates="articles", link_model=UserArticleLink)
    authors: List["Author"] = Relationship(back_populates="articles", link_model=ArticleAuthorLink)
    tags: List["Tag"] = Relationship(back_populates="articles", link_model=ArticleTagLink)
    comments: List["Comment"] = Relationship(back_populates="article", link_model=ArticleCommentLink)

class Author(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    articles: List[Article] = Relationship(back_populates="authors", link_model=ArticleAuthorLink)

class Tag(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    articles: List[Article] = Relationship(back_populates="tags", link_model=ArticleTagLink)

class Comment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
    article: Article = Relationship(back_populates="comments", link_model=ArticleCommentLink)
    user: User = Relationship(back_populates="comments", link_model=UserCommentLink)