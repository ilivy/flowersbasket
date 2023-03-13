from ariadne.asgi import GraphQL
from starlette.requests import Request

from app.db.session import get_database
from app.web.api.schema import schema


async def get_context_value(request: Request, _):
    db_session = get_database()

    return {
        "request": request,
        "db_session": db_session,
    }


server = GraphQL(schema, context_value=get_context_value, debug=True)
