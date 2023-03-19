from rest_framework import viewsets, mixins

from .serializers import (
    TitleSerializer, GenreSerializer, CategorySerializer,
    CommentSerializer, ReviewSerializer)
from titles.models import Title, Genre, Category, Review
from django.shortcuts import get_object_or_404


class TitleViewSet(viewsets.ModelViewSet):
    """Представление модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Представление модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Представление модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление модели Review."""
    serializer_class = ReviewSerializer
    # TODO: permission_classes = ...

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    # TODO: permission_classes = ...

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
