from sqlmodel import Session, create_engine
from tables import User, Author, Article, Tag
from datetime import date

engine = create_engine("sqlite:///./test.db")

def add_sample_data():
    with Session(engine) as session:
        # Add users
        user1 = User(username="user1", hashed_password="password1")
        user2 = User(username="user2", hashed_password="password2")
        
        session.add_all([user1, user2])
        session.commit()

        # Add authors
        author1 = Author(name="Author One")
        author2 = Author(name="Author Two")
        
        session.add_all([author1, author2])
        session.commit()

        # Add tags
        tag1 = Tag(name="Technology")
        tag2 = Tag(name="Health")
        
        session.add_all([tag1, tag2])
        session.commit()

        # Add articles and associate with users, authors, and tags
        article1 = Article(
            title="Article 1",
            abstract="Abstract of Article 1",
            publication_date=date(2023, 1, 1),
            user=user1,
            authors=[author1],
            tags=[tag1]
        )
        article2 = Article(
            title="Article 2",
            abstract="Abstract of Article 2",
            publication_date=date(2023, 2, 1),
            user=user2,
            authors=[author2],
            tags=[tag2]
        )

        session.add_all([article1, article2])
        session.commit()

