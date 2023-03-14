from app.models import Schedule, OrderItem, Status


def order_created(data):
    schedule = Schedule.objects.create(
        order_id=data['order_id'],
        status=Status.CREATED
    )

    for data_item in data["items"]:
        OrderItem.objects.create(
            product=data_item["product"],
            size=data_item["size"],
            quantity=int(data_item["quantity"]),
            schedule=schedule)
