from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from dry_rest_permissions.generics import authenticated_users


class User(AbstractUser):
    """
    Default custom user model for Rakuten Management.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    service_secret = CharField(
        _("service Secret"),
        blank=True,
        null=True,
        max_length=255
    )
    license_key = CharField(
        _("license Key"),
        blank=True,
        null=True,
        max_length=255
    )

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @authenticated_users
    def has_read_permission(request):
        return True
    
    @authenticated_users
    def has_write_permission(request):
        return True

    @authenticated_users
    def has_object_write_permission():
        return True

    def has_register_permission(request):
        return True

    def has_login_permission(request):
        return True
