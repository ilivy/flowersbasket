# Generated by Django 4.1.7 on 2023-03-14 05:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="schedule",
            name="app_schedul_created_b58d6e_idx",
        ),
        migrations.AddIndex(
            model_name="schedule",
            index=models.Index(
                fields=["order_id"], name="app_schedul_order_i_f6c0ba_idx"
            ),
        ),
    ]
