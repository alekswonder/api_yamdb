from rest_framework import viewsets

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from titles.models import Title, Genre, Category


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # TODO: permission_classes = ...
    # TODO: pagination_class = ...
