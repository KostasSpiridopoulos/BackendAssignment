import uvicorn
from sqlmodel import SQLModel, create_engine
from fastapi import FastAPI
import auth
import articles
import comments
from sample_data import add_sample_data

engine = create_engine("sqlite:///./test.db")
SQLModel.metadata.create_all(engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(comments.router)
#add_sample_data()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)