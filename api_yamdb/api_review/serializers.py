from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Review, Comment
from api_titles.models import Titles  # noqa


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title = get_object_or_404(
            Titles, id=serializer_field.context['title_id'])
        return title


class CurrentReviewDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title = get_object_or_404(
            Titles, id=serializer_field.context['title_id'])
        review = get_object_or_404(
            Review,
            id=serializer_field.context['review_id'],
            title=title)
        return review


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    title = serializers.HiddenField(default=CurrentTitleDefault())

    def validate_score(self, value):
        if value > 10 or value < 1:
            raise serializers.ValidationError('Incorrect score')
        return value

    class Meta:
        model = Review
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
            ),
        )


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    review = serializers.HiddenField(default=CurrentReviewDefault())

    class Meta:
        model = Comment
        fields = '__all__'
