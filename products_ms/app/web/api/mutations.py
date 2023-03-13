import copy
import uuid
from datetime import datetime

from ariadne import MutationType

from app.web.api.exception import ItemNotFoundError

mutation = MutationType()


@mutation.field("addSupplier")
def resolve_add_supplier(_, info, name, input):
    db = info.context["db_session"]
    collection = db.suppliers
    input["name"] = name
    input["_id"] = str(uuid.uuid4())
    collection.insert_one(input)
    return input


@mutation.field("addFlower")
def resolve_add_flower(_, info, name, input):
    db = info.context["db_session"]
    collection = db["flowers"]
    input["name"] = name
    input["_id"] = str(uuid.uuid4())
    input["updatedAt"] = datetime.utcnow().isoformat()
    collection.insert_one(input)
    return input


@mutation.field("addProduct")
def resolve_add_product(_, info, name, type, input):
    db = info.context["db_session"]
    collection = db["products"]
    product = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "available": input.get("available", False),
        "flowers": input.get("flowers", []),
        "updatedAt": datetime.utcnow().isoformat(),
    }
    if type == "bouquet":
        product.update(
            {
                "hasRibbon": input.get("hasRibbon", False),
            }
        )
    else:
        product.update(
            {
                "hasHandle": input.get("hasHandle", False),
            }
        )
    collection.insert_one(product)
    return product


@mutation.field("updateProduct")
def resolve_update_product(_, info, _id, input):
    db = info.context["db_session"]
    collection = db["products"]
    upd = copy.copy(input)
    upd["updatedAt"] = str(datetime.utcnow())
    filter = {"_id": _id}
    newvalues = {"$set": upd}
    collection.update_one(filter, newvalues)
    updated = collection.find_one({"_id": _id})
    if updated:
        return updated
    raise ItemNotFoundError(f"Product with ID {_id} not found")


@mutation.field("deleteProduct")
def resolve_delete_product(_, info, _id):
    db = info.context["db_session"]
    collection = db["products"]
    if not collection.find_one({"_id": _id}):
        raise ItemNotFoundError(f"Product with ID {_id} not found")
    collection.delete_one({"_id": _id})
    return True


@mutation.field("updateStock")
def resolve_update_stock(_, info, _id, changeAmount):
    db = info.context["db_session"]
    collection = db["flowers"]
    filter = {"_id": _id}
    newvalues = {"$set": {"stock": changeAmount}}
    collection.update_one(filter, newvalues)
    updated = collection.find_one({"_id": _id})
    if updated:
        return updated
    raise ItemNotFoundError(f"Flower with ID {_id} not found")
