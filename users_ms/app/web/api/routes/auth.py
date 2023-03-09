from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.repository.users_repository import UsersRepository
from app.repository.unit_of_work import UnitOfWork
from app.users_service.users_service import UsersService
from app.users_service.users import User
from app.web.api.schemas import UserRegisterInSchema, UserOutSchema, Token
from app.web.api.auth import authenticate_user, issue_new_token, get_current_user

router = APIRouter(tags=["auth"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserOutSchema
)
async def register(payload: UserRegisterInSchema):
    with UnitOfWork() as unit_of_work:
        repo = UsersRepository(unit_of_work.session)
        users_service = UsersService(repo)
        # user ID didn't exist before commit
        # we have to get it now when the SQLAlchemy session is still active.
        user_data = payload.dict()
        del user_data["password_confirm"]
        user = users_service.add_user(**user_data)
        unit_of_work.commit()
        res = user.dict()
    return res


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = issue_new_token(user)
    return token


@router.get("/current_user", response_model=UserOutSchema)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user.dict()
