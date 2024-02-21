# Generated by Django 4.1.7 on 2023-03-14 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="KafkaError",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
                ("error", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("product", models.CharField(max_length=250)),
                ("size", models.CharField(max_length=64)),
                ("quantity", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("order_id", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("CR", "Created"), ("RD", "Ready")],
                        default="CR",
                        max_length=2,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="schedule",
            index=models.Index(
                fields=["-created_at"], name="app_schedul_created_b58d6e_idx"
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="schedule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_items",
                to="app.schedule",
            ),
        ),
    ]