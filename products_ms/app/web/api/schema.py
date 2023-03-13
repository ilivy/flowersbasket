from pathlib import Path

from ariadne import make_executable_schema

from app.web.api.queries import query
from app.web.api.mutations import mutation
from app.web.api.types import (
    datetime_scalar,
    product_type,
    product_interface,
    flower_type,
    supplier_type,
)


schema = make_executable_schema(
    (Path(__file__).parent / "products.graphql").read_text(),
    [
        query,
        mutation,
        product_interface,
        product_type,
        flower_type,
        supplier_type,
        datetime_scalar,
    ],
)
