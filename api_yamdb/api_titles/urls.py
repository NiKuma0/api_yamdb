from django.urls import path, include

from .views import some_view

urlpatterns = [
    path('v1/titles/', some_view),
    path('', include('api_review.urls'))
]
