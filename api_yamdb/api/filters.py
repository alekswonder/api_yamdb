from django_filters import filters
from django_filters.rest_framework import FilterSet
from titles.models import Title


class TitleFilterSet(FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    name = filters.CharFilter(field_name='name')
    year = filters.CharFilter(field_name='year')

    class Meta:
        model = Title
        fields = '__all__'
