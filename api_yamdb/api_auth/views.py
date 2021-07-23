from rest_framework import status, viewsets, permissions, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from django.contrib.auth import get_user_model

from .permissions import IsAdmin
from .serializers import TokenSerializer, AuthSerializer, UserSerializer

User = get_user_model()


class TokenView(TokenViewBase):
    serializer_class = TokenSerializer


def authorization(user, serializer):
    user.set_confirmation_code()
    confirmation_code = user._confirmation_code
    user.save(update_fields=('confirmation_code',))
    user.email_user(
        user.get_full_name(),
        f'Ваш код: {confirmation_code}'
    )
    return Response({
        serializer.data.get('email'): 'Проверьте свою почту'
    })


def registration(serializer):
    user = User.objects.create_user(
        username=User.make_random_username(),
        **serializer.data)
    user.set_confirmation_code()
    user.email_user(
        user.get_full_name(),
        ('Регистрация прошла успешно!\n'
         'Для выс мы сгенерировали пароль и никнейм!\n'
         f'Ваш никнейм: {user.username}\n'
         f'Ваш код: {user._confirmation_code}')
    )
    user.save(update_fields=('confirmation_code',))
    return Response({
        serializer.data.get('email'): 'Проверьте свою почту'},
        status=status.HTTP_201_CREATED
    )


class AuthVIew(APIView):
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return registration(serializer)
        return authorization(user, serializer)


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
