from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrderConfig(AppConfig):
    name = "rakuten_mng.order"
    verbose_name = _("Order")
