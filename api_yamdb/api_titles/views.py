from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions
from rest_framework.filters import SearchFilter

from api_auth.permissions import IsAdmin  # noqa
from .models import Categories, Genres, Titles
from .serializer import CategoriesSerializer, GenresSerializer, TitlesSerializer


class RestViewSets(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    pass
    

class CategoriesViewSet(RestViewSets):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = (IsAdmin,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return super(CategoriesViewSet, self).get_permissions()


class GenresViewSet(RestViewSets):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
