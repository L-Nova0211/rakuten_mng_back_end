# Generated by Django 4.2.4 on 2023-10-18 09:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0006_productsetting_created_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="manage_number",
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="manage Number"),
        ),
        migrations.AddField(
            model_name="product",
            name="point",
            field=models.IntegerField(blank=True, null=True, verbose_name="point"),
        ),
        migrations.AddField(
            model_name="product",
            name="profit",
            field=models.IntegerField(blank=True, null=True, verbose_name="profit"),
        ),
        migrations.AddField(
            model_name="product",
            name="rakuten_fee",
            field=models.IntegerField(blank=True, null=True, verbose_name="rakuten Fee"),
        ),
        migrations.AddField(
            model_name="product",
            name="shipping_fee",
            field=models.IntegerField(blank=True, null=True, verbose_name="shipping Fee"),
        ),
        migrations.AlterField(
            model_name="productsetting",
            name="rakuten_fee",
            field=models.IntegerField(
                choices=[(0, "Zero"), (8, "Eight"), (10, "Ten")], default=10, verbose_name="rakuten Fee"
            ),
        ),
    ]
