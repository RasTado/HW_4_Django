from django_filters import rest_framework as filters

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet, filters.DjangoFilterBackend):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры

    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'created_at']
