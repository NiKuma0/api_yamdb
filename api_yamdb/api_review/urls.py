from django.urls import path

from .views import some_view

urlpatterns = [
    path('v1/titles/review/', some_view),
]
