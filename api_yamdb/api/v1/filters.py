import django_filters
from reviews.models import Titles


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    genres = django_filters.CharFilter(field_name='genres__slug')
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Titles
        fields = ('category', 'genres', 'name', 'year')
