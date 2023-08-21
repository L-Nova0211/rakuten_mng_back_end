from django.contrib.auth import get_user_model
from rest_framework import serializers

from rakuten_mng.users.models import User as UserType


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
        ]
