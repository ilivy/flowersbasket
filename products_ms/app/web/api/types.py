import copy

from ariadne import InterfaceType, ObjectType, ScalarType, UnionType

product_interface = InterfaceType("ProductInterface")
product_type = UnionType("Product")
flower_type = ObjectType("Flower")
supplier_type = ObjectType("Supplier")

datetime_scalar = ScalarType("Datetime")


@product_type.type_resolver
def resolve_product_type(obj, *_):
    """
    Whenever a query or mutation returns multiple types, you’ll need to
    implement a type resolver.
    This applies to queries and mutations that return union types
    and object types that implement interfaces.
    """
    if "hasHandle" in obj:
        return "Basket"
    return "Bouquet"


@product_interface.field("flowers")
def resolve_product_flowers(product, info):
    """Replaces Flower ID with Flower Obj"""
    db = info.context["db_session"]
    collection = db.flowers
    flower_list_data = [copy.copy(flower) for flower in product.get("flowers", [])]
    for flower_data in flower_list_data:  # data from the request
        flower_data["flower"] = collection.find_one({"_id": flower_data["flower"]})
    return flower_list_data


@flower_type.field("supplier")
def resolve_flower_supplier(flower, info):
    """Replaces Supplier ID with Supplier Obj"""
    if flower.get("supplier") is not None:
        db = info.context["db_session"]
        collection = db.suppliers
        supplier = collection.find_one({"_id": flower.get("supplier")})
        return supplier


@flower_type.field("products")
def resolve_flower_products(flower, info):
    """Fills in 'products' list"""
    db = info.context["db_session"]
    prod_collection = db.products
    res_products = []
    for product_db_obj in prod_collection.find():
        for product_flower in product_db_obj.get("flowers", []):
            if product_flower["flower"] == flower["_id"]:
                res_products.append(product_db_obj)
    return res_products


@supplier_type.field("flowers")
def resolve_supplier_flowers(supplier, info):
    db = info.context["db_session"]
    collection = db.flowers
    return collection.find({"supplier": supplier["_id"]})


@datetime_scalar.serializer
def serialize_datetime_scalar(dt: str):
    # def serialize_datetime_scalar(dt: datetime):
    # return dt.isoformat()
    return dt


@datetime_scalar.value_parser
def parse_datetime_scalar(dt):
    # return datetime.fromisoformat(dt)
    return dt
