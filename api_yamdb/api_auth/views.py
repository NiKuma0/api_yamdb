from rest_framework import viewsets, permissions, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from django.contrib.auth import get_user_model

from .permissions import IsAdmin
from .serializers import TokenSerializer, AuthSerializer, UserSerializer

User = get_user_model()


class TokenView(TokenViewBase):
    serializer_class = TokenSerializer


class AuthVIew(APIView):
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_or_create(**serializer.data)
        user.set_confirmation_code()
        user.email_user(
            user.get_full_name(),
            f'Ваш код: {user._confirmation_code}'
        )
        user.save(update_fields='confirmation_code')
        return Response(
            data={'email': user.email}
        )


class UserMeView(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    def get_serializer(self, *args, **kwargs):
        serializer = self.serializer_class
        serializer.Meta.read_only_fields = []
        return serializer(*args, **kwargs)
