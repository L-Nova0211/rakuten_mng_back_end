# Generated by Django 4.2.4 on 2023-11-07 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0009_alter_productsetting_rakuten_fee"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.IntegerField(blank=True, null=True, verbose_name="status")),
                ("order_date", models.DateField(blank=True, null=True, verbose_name="order Date")),
                ("order_number", models.CharField(blank=True, max_length=255, null=True, verbose_name="order Number")),
                ("item_id", models.IntegerField(blank=True, null=True, verbose_name="item ID")),
                (
                    "product",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="product.product"
                    ),
                ),
            ],
        ),
    ]
