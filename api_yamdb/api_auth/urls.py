from django.urls import path
from .views import TokenView, auth_view

urlpatterns = [
    path('v1/auth/email/', auth_view),
    path('v1/auth/token/', TokenView.as_view(), name='token_obtain_pair'),
]
