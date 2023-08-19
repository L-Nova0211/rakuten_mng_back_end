from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "rakuten_mng.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import rakuten_mng.users.signals  # noqa: F401
        except ImportError:
            pass
