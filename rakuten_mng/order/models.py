from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    class Status(models.IntegerChoices):
        WATINGORDERCONFIRM = 100
        RAKUTENPROCESSING = 200
        WATINGSHIP = 300
        WAITINGCHANGECONFIRM = 400
        SHIPPED = 500
        PAYMENTPROCESSING = 600
        PAYMENTCOMPLETE = 700
        WAITINGCANCELCONFIRM = 800
        CANCELCONFIRM = 900

    status = models.IntegerField(
        _("status"),
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        "product.Product",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    order_date = models.DateField(
        _("order Date"),
        null=True,
        blank=True,
    )
    order_number = models.CharField(
        _("order Number"),
        max_length=255,
        null=True,
        blank=True
    )
    item_id = models.IntegerField(
        _("item ID"),
        null=True,
        blank=True
    )
