from django.db import models


class Status(models.TextChoices):
    CREATED = "CR", "Created"
    PUBLISHED = "RD", "Ready"


class Schedule(models.Model):
    order_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.CREATED
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_id"]),
        ]

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.CharField(max_length=250)
    size = models.CharField(max_length=64)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product[:64]


class KafkaError(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    error = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
