from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions

from rakuten_mng.product.models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    permission_classes = (DRYPermissions, )
    queryset = Product.objects.all()
    filterset_fields = ['status']
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user)
