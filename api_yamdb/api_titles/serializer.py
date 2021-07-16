from django.db.models import fields
from rest_framework import serializers

from api_titles.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    fields = "__all__"
    model = Categories


class GenresSerializer(serializers.ModelSerializer):
    fields = "__all__"
    model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), 
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Titles
