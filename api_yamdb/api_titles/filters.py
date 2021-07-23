from django_filters import rest_framework

from .models import Titles


class FilterSetTitle(rest_framework.FilterSet):
    name = rest_framework.CharFilter(field_name='name',
                                     lookup_expr='contains')
    category = rest_framework.CharFilter(field_name='category__slug',
                                         lookup_expr='exact')
    genre = rest_framework.CharFilter(field_name='genre__slug',
                                      lookup_expr='exact')

    class Meta:
        fields = ('name', 'genre', 'category', 'year')
        model = Titles
