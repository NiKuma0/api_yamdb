from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoriesViewSet, GenresViewSet, TitleViewSet


router = DefaultRouter()
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoriesViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include('api_review.urls')),
]
