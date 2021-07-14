from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import TokenSerializer, AuthSerializer, UserSerializer
from .managers import UserManager

User = get_user_model()


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer


@api_view(http_method_names=['POST'])
def auth_view(request):
    serialized = AuthSerializer(data=request.data)
    if not serialized.is_valid():
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=request.data.get('email'))
        password = UserManager.make_random_password(user)
        user.set_password(password)
        return Response({serialized.data.get('email'): 'Проверьте свою почту'})
    except User.DoesNotExist:
        User.objects.create_user(
            email=serialized.data.get('email'),
        )
        return Response({serialized.data.get('email'): 'Проверьте свою почту'}, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
