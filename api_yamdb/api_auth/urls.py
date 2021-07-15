from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TokenView, AuthVIew, UserMeView, UsersView

users_router = DefaultRouter()
users_router.register(r'users', UsersView, basename='user')


urlpatterns = [
    path('v1/auth/email/', AuthVIew.as_view()),
    path('v1/auth/token/', TokenView.as_view(), name='token_obtain_pair'),
    path('v1/users/me/', UserMeView.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='users_me'),
    path('v1/', include(users_router.urls)),
    # path('v1/users/me/', UserMeView.as_view({'get': 'retrieve', 'patch': 'update'})),
]
