from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductConfig(AppConfig):
    name = "rakuten_mng.product"
    verbose_name = _("Product")

