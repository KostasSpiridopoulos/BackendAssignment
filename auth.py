from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session, select, create_engine
from starlette import status
from tables import User
from models import CreateUserRequest, Token

router = APIRouter(prefix="/auth", 
                    tags=["auth"])


SECRET_KEY = "1232341235123451234514325aaeqw1234312"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine("sqlite:///./test.db")
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, 
                      session: Session = Depends(get_session)):
    
    create_user_model = User(username=create_user_request.username,
                             hashed_password=bcrypt_context.hash(create_user_request.password),
                             )

    session.add(create_user_model)
    session.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(username: str, password: str, session: Session) -> bool|User:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).one()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    expires = datetime.now() + expires_delta
    encode = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
 
async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
