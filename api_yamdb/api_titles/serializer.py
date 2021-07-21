from django.db.models import fields
from rest_framework import serializers
# from rest_framework.validators import

from .models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    # genre = GenresSerializer(many=True)
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Titles
        relations = ('category',)

    def create(self, validated_data):
        genre = validated_data.pop('genre', (None,))
        instance = super(TitlesSerializer, self).create(validated_data)
        genre = Genres.objects.filter(slug__in=genre)
        instance.genre.set(genre)
        return instance
# "genre": ["action", "fps"]
