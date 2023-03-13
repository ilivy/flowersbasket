from itertools import islice

from ariadne import QueryType

from app.web.api.exception import ItemNotFoundError

query = QueryType()


def get_page(items, items_per_page, page):
    page -= 1
    start = items_per_page * page
    stop = start + items_per_page
    return list(islice(items, start, stop))


@query.field("allSuppliers")
def resolve_all_suppliers(_, info):
    db = info.context["db_session"]
    collection = db.suppliers
    return collection.find()


@query.field("allFlowers")
def resolve_all_flowers(_, info):
    db = info.context["db_session"]
    collection = db.flowers
    return collection.find()


@query.field("allProducts")
def resolve_all_products(_, info):
    db = info.context["db_session"]
    collection = db.products
    return collection.find()


@query.field("products")
def resolve_products(_, info, input=None):
    db = info.context["db_session"]
    collection = db.products
    filtered = collection.find()
    if input is None:
        return filtered
    filtered = [
        product for product in filtered if product["available"] is input["available"]
    ]
    if input.get("minPrice") is not None:
        filtered = [
            product for product in filtered if product["price"] >= input["minPrice"]
        ]
    if input.get("maxPrice") is not None:
        filtered = [
            product for product in filtered if product["price"] <= input["maxPrice"]
        ]
    filtered.sort(
        key=lambda product: product[input["sortBy"]],
        reverse=input["sort"] == "DESCENDING",
    )
    return get_page(filtered, input["resultsPerPage"], input["page"])


@query.field("product")
def resolve_product(_, info, _id):
    db = info.context["db_session"]
    collection = db.products
    product = collection.find_one({"_id": _id})
    if product:
        return product
    raise ItemNotFoundError(f"Product with ID {_id} not found")


@query.field("flower")
def resolve_flower(_, info, _id):
    db = info.context["db_session"]
    collection = db.flowers
    flower = collection.find_one({"_id": _id})
    if flower:
        return flower
    raise ItemNotFoundError(f"Flower with ID {_id} not found")
