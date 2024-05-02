from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select, create_engine
from starlette import status
from tables import User, Article, Comment, ArticleCommentLink
from models import CommentCreate, CommentDelete, CommentUpdate
from auth import get_current_user
from typing import List
from starlette import status

router = APIRouter(prefix="/comments", 
                    tags=["comments"])

engine = create_engine("sqlite:///./test.db")
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/get_comments", response_model=List[Comment])
async def get_comment(article_id: int=None,
                      session: Session = Depends(get_session)):
    statement = select(Comment)\
                    .join(ArticleCommentLink, Comment.id == ArticleCommentLink.comment_id)\
                    .where(ArticleCommentLink.article_id == article_id)
    comments = session.exec(statement).all()
    print(comments)
    return comments

@router.post("/add_comment", response_model=Comment)
async def add_comment(request: CommentCreate,
                      user: dict = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    article = session.get(Article, request.article_id)
    user = session.get(User, user["id"])

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not found.")
    
    comment = Comment(content=request.content,
                      article=article,
                      user=user)
    session.add(comment)
    session.commit()
    return comment

@router.post("/update_comment", response_model=Comment)
async def update_comment(request: CommentUpdate,
                         user: dict = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    comment = session.get(Comment, request.comment_id)
    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment not found.")
    if comment.user.id != user["id"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized action.")
    comment.content = request.content
    session.commit()
    return comment

@router.delete("/delete_comment", status_code=204)
async def delete_comment(request: CommentDelete,
                         user: dict = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    
    comment = session.get(Comment, request.comment_id)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment not found.")
    if comment.user.id != user["id"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized action.")
    session.delete(comment)
    session.commit()
    return {"message": "Comment deleted."}

