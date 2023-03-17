from rest_framework import viewsets, mixins

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from titles.models import Title, Genre, Category


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...
