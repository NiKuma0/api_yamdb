from rest_framework import status, viewsets, permissions, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .permissions import IsAdmin
from .serializers import TokenSerializer, AuthSerializer, UserSerializer
from .managers import UserManager

User = get_user_model()


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer


class AuthVIew(APIView):
    serializer_class = AuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=request.data.get('email'))
            password = UserManager.make_random_password(user)
            user.set_password(password)
            user.save()
            return Response({serializer.data.get('email'): 'Проверьте свою почту'})
        except User.DoesNotExist:
            User.objects.create_user(**serializer.data)
            return Response({serializer.data.get('email'): 'Проверьте свою почту'}, status=status.HTTP_201_CREATED)


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

