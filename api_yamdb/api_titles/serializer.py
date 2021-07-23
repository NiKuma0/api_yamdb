from rest_framework import serializers
from django.db.models import Avg

from .models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Titles
        relations = ('category',)

    def to_representation(self, instance):
        res = super(TitlesSerializer, self).to_representation(instance)
        res['category'] = CategoriesSerializer(instance=instance.category).data
        res['genre'] = GenresSerializer(
            instance=instance.genre, many=True).data
        return res

    @staticmethod
    def get_rating(obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']
