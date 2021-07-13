from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import TokenSerializer, AuthSerializer
from .managers import UserManager

User = get_user_model()


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer


@api_view(http_method_names=['POST'])
def auth_view(request):
    serialized = AuthSerializer(data=request.data)
    if not serialized.is_valid():
        if not serialized.errors['email'][0].code == 'unique':
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=request.data.get('email'))
        password = UserManager.make_random_password(user)
        user.set_password(password)
        return Response({serialized.data.get('email'): 'Проверьте свою почту'})
    User.objects.create_user(
        email=serialized.data.get('email'),
    )
    return Response({serialized.data.get('email'): 'Проверьте свою почту'}, status=status.HTTP_201_CREATED)
