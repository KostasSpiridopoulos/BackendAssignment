from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import SQLModel, Session, select, create_engine
from starlette import status
from tables import User, Article, Tag, Author, ArticleAuthorLink, ArticleTagLink
from models import ArticleCreate, ArticleDelete, ArticleUpdate, AuthorCreate, TagCreate
from auth import get_current_user
from typing import List, Optional
from starlette import status
from sqlalchemy import func, or_, and_
import csv
from io import StringIO

PAGE_LIMIT = 100

router = APIRouter(prefix="/articles", 
                    tags=["articles"])

engine = create_engine("sqlite:///./test.db")
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/add_author", response_model=Author)
async def add_author(request: AuthorCreate,
                     session: Session = Depends(get_session)):
    author = Author(name=request.name)
    session.add(author)
    session.commit()
    return author

@router.get("/get_authors", response_model=List[Author])
async def get_authors(session: Session = Depends(get_session)):
    authors = session.exec(select(Author)).all()
    return authors

@router.post("/add_tag", response_model=Tag)
async def add_tag(request: TagCreate,
                  session: Session = Depends(get_session)):
    tag = Tag(name=request.name)
    session.add(tag)
    session.commit()
    return tag

@router.get("/get_tags", response_model=List[Tag])
async def get_tags(session: Session = Depends(get_session)):
    tags = session.exec(select(Tag)).all()
    return tags

@router.post("/add_article", response_model=Article)
async def add_article(request: ArticleCreate, 
                      user: dict = Depends(get_current_user), 
                      session: Session = Depends(get_session)):
    article = Article(title=request.title, 
                      abstract=request.abstract, 
                      publication_date=request.publication_date,
                      user=session.get(User, user["id"]))
    
    for author_id in request.authors:
        author = session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Author with id: {author_id} was not found.")
        article.authors.append(author)

    for tag_id in request.tags:
        tag = session.get(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Tag with id: {tag_id} was not found.")
        article.tags.append(tag)

    session.add(article)
    session.commit()
    return article

@router.put("/update_article", response_model=Article)
async def update_article(request: ArticleUpdate,
                         user: dict = Depends(get_current_user), 
                         session: Session = Depends(get_session)):
    article = session.get(Article, request.article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not found.")
    if article.user.id != user["id"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthoriazed action.")
    
    article.title = request.title
    article.abstract = request.abstract
    article.publication_date = request.publication_date

    updated_authors = []
    for author_id in request.authors:
        author = session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Author with id: {author_id} was not found.")
        updated_authors.append(author)
    article.authors = updated_authors

    updated_tags = []
    for tag_id in request.tags:
        tag = session.get(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Tag with id: {tag_id} was not found.")
        updated_tags.append(tag)
    article.tags = updated_tags
    session.commit()

    return article

@router.delete("/delete_article", status_code=204)
async def delete_article(request: ArticleDelete,
                         user: dict = Depends(get_current_user), 
                         session: Session = Depends(get_session)):
    article = article = session.get(Article, request.article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not.")
    if article.user.id != user["id"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthoriazed action.")
    
    session.delete(article)
    session.commit()
    return {"message": "User deleted successfuly"}

@router.get("/get_all_articles", response_model=List[Article])
async def get_all_articles(session: Session = Depends(get_session)):
    articles = session.exec(select(Article)).all()
    return articles

@router.get("/get_filtered_articles", response_model=List[Article])
async def get_filtered_articles(year: Optional[str] = None, 
                                month: Optional[str] = None, 
                                authors: Optional[str] = None,
                                tags: Optional[str] = None,
                                keywords: Optional[str] = None,
                                page: int = Query(1, ge=1),
                                session: Session = Depends(get_session)):
    fitlered_articles = get_filtered_articles(year, month, authors, tags, keywords, session, page)
    return fitlered_articles

@router.get("/download_filtered_articles", response_class=Response)
async def download_filtered_articles(year: Optional[str] = None, 
                                     month: Optional[str] = None, 
                                     authors: Optional[str] = None,
                                     tags: Optional[str] = None,
                                     keywords: Optional[str] = None,
                                     session: Session = Depends(get_session)):
    articles = get_filtered_articles(year, month, authors, tags, keywords, session)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")
    
    stream = StringIO()
    csv_writer = csv.writer(stream)
    csv_writer.writerow(['id', 'title', 'abstract'])

    for article in articles:
        csv_writer.writerow([article.id, article.title, article.abstract])
    
    stream.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="articles.csv"'
    }

    return Response(content=stream.getvalue(), media_type="text/csv", headers=headers)

@router.get("/download_articles", response_class=Response)
async def download_filtered_articles(article_ids: Optional[str] = None, 
                                     session: Session = Depends(get_session)):
    
    article_ids = [int(aritcle_id.strip()) for aritcle_id in article_ids.split(",")]

    statement = select(Article).where(Article.id.in_(article_ids))
    articles = session.exec(statement).all()

    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")
    
    stream = StringIO()
    csv_writer = csv.writer(stream)
    csv_writer.writerow(['id', 'title', 'abstract'])

    for article in articles:
        csv_writer.writerow([article.id, article.title, article.abstract])
    
    stream.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="articles.csv"'
    }

    return Response(content=stream.getvalue(), media_type="text/csv", headers=headers)

def get_filtered_articles(year: str, 
                          month:str, 
                          authors:str, 
                          tags:str,
                          keywords: str, 
                          session: Session,
                          page: int = None) -> List[Article]:
    statement = select(Article)
    if year: 
        statement = statement.where(func.strftime('%Y', Article.publication_date) == year)
    if month:
        statement = statement.where(func.strftime('%m', Article.publication_date) == month)
    if authors:
        authors = set([author.strip() for author in authors.split(",")])
        statement = statement\
                        .join(ArticleAuthorLink, Article.id == ArticleAuthorLink.article_id)\
                        .join(Author, Author.id == ArticleAuthorLink.author_id)\
                        .where(Author.name.in_(authors))\
                        .group_by(Article.id)\
                        .having(func.count(func.distinct(Author.name)) == len(authors))
    if tags:
        tags = set([tag.strip() for tag in tags.split(",")])
        statement = statement\
                        .join(ArticleTagLink, Article.id == ArticleTagLink.article_id)\
                        .join(Tag, Tag.id == ArticleTagLink.tag_id)\
                        .where(Tag.name.in_(tags))\
                        .group_by(Article.id)\
                        .having(func.count(func.distinct(Tag.name)) == len(tags))
    if keywords:
        keywords = [keyword.strip() for keyword in keywords.split(",")]
        or_conditions = [Article.title.ilike(f"%{keyword}%") | Article.abstract.ilike(f"%{keyword}%") for keyword in keywords]
        statement = statement.where(and_(*or_conditions))

    if not page:
        articles = session.exec(statement).all()
    else:
        articles = session.exec(statement.offset((page - 1) * PAGE_LIMIT).limit(PAGE_LIMIT)).all()

    for art in articles:
        print(art.authors, art.tags)
    return articles

# na kanw to read me
# gia to readme na valw requirements txt me ta modules kai na pw na trekseis to main na pas sto swagger kai na dokimaseis a APIs
# UNIT TESTING
