import os
import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.web.api.routes.api import router
from app.config import settings

os.environ["TZ"] = settings.TIMEZONE
time.tzset()


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
    )
    application.include_router(router, prefix=settings.API_V1_STR)
    return application


app = get_application()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3030",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def main():
    return {"status": "ok"}
