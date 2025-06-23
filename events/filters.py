import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    date = django_filters.IsoDateTimeFilter(field_name='date')
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    year_gte = django_filters.NumberFilter(field_name='date', lookup_expr='year__gte')
    year_lte = django_filters.NumberFilter(field_name='date', lookup_expr='year__lte')
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    month_gte = django_filters.NumberFilter(field_name='date', lookup_expr='month__gte')
    month_lte = django_filters.NumberFilter(field_name='date', lookup_expr='month__lte')
    day = django_filters.NumberFilter(field_name='date', lookup_expr='day')
    day_gte = django_filters.NumberFilter(field_name='date', lookup_expr='day__gte')
    day_lte = django_filters.NumberFilter(field_name='date', lookup_expr='day__lte')

    class Meta:
        model = Event
        fields = ['category', 'date']
