from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt, ExpiredSignatureError
from passlib.context import CryptContext

from app.config import settings
from app.users_service.users import User
from app.repository.users_repository import UsersRepository
from app.repository.models import UserModel
from app.repository.unit_of_work import UnitOfWork
from app.web.api.schemas import TokenData


JWT_SECRET = settings.JWT_SECRET  # to get a random string run: <openssl rand -hex 32>
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> UserModel:
    with UnitOfWork() as unit_of_work:
        repo = UsersRepository(unit_of_work.session)
        user = repo.find_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def issue_new_token(user: UserModel):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWSError, ExpiredSignatureError):
        raise credentials_exception
    with UnitOfWork() as unit_of_work:
        repo = UsersRepository(unit_of_work.session)
        user = repo.find_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return User(**user.dict())
