from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api_titles.models import Titles  # noqa
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import ReviewAndCommentPermissions
from .models import Review


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = (ReviewAndCommentPermissions,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs.get('title_id')
        return context

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (ReviewAndCommentPermissions,)

    def __get_review(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=title)
        return review

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs.get('title_id')
        context['review_id'] = self.kwargs.get('review_id')
        return context

    def get_queryset(self):
        review = self.__get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.__get_review()
        serializer.save(author=self.request.user, review=review)
