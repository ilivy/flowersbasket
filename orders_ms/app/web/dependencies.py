import httpx

from fastapi import Header, HTTPException, status

from app.repository.database import session
from app.config import settings
from app.web.api.schemas import UserSchema

USERS_MS_URL = settings.USERS_MS_URL


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(authorization: str = Header()) -> UserSchema:
    """Gets current user via 'users' microservice
    using 'Password' OAuth2 flow
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not authorization:
        raise credentials_exception

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": authorization}
        try:
            r = await client.get(USERS_MS_URL + "/current_user", headers=headers)
        except httpx.HTTPError as exc:
            raise credentials_exception

        if not r.status_code == httpx.codes.OK:
            raise credentials_exception

        return r.json()
