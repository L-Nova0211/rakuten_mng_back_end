from django.contrib.auth import get_user_model, authenticate, login
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from dry_rest_permissions.generics import DRYPermissions

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (DRYPermissions, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        user_exist = User.objects.filter(Q(email=request.data['email']) | Q(username=request.data['username'])).first()
        if not user_exist:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                User.objects.create_user(**serializer.validated_data)
                return Response(status=200)
            
            return Response(
                data='入力した情報が正しくありません。',
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                data='同じメールを持つユーザーが既に存在します。',
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['POST'])
    def login(self, request):
        user = authenticate(request=request, email=request.data['email'], password=request.data['password'])
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': self.serializer_class(user).data
            }
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data='メールやパスワードが正しくありません。',
                status=status.HTTP_401_UNAUTHORIZED
            )
