from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from rakuten_mng.product.api.views import ProductViewSet
from rakuten_mng.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("product", ProductViewSet)
router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
