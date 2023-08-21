from rest_framework import serializers

from rakuten_mng.product.models import Product, ProductPhoto
from rakuten_mng.users.api.serializers import UserSerializer


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    productphoto_set = ProductPhotoSerializer(
        many=True, read_only=False, required=False
    )

    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1
