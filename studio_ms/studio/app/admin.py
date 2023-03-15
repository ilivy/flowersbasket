from django.contrib import admin
from .models import Schedule, OrderItem, KafkaError


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Schedule)
class PostAdmin(admin.ModelAdmin):
    list_display = ["order_id", "status", "created_at", "updated_at"]
    list_filter = ["order_id", "status", "created_at"]
    search_fields = ["order_id"]
    ordering = ["status", "created_at"]
    inlines = [
        OrderItemInline,
    ]


@admin.register(KafkaError)
class PostAdmin(admin.ModelAdmin):
    list_display = ["key", "created_at"]
    list_filter = ["created_at"]
    ordering = ["created_at"]
