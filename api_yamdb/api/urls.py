from django.urls import re_path, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    re_path(r'^api-token-auth/', obtain_jwt_token),
]
