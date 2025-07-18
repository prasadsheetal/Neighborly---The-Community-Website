import django_filters
from .models import ServiceItem


class ServiceItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    service_provider = django_filters.NumberFilter()

    # price
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    # dates
    date_posted = django_filters.DateFilter(field_name="date_posted")  # exact
    date_posted__gte = django_filters.DateFilter(
        field_name="date_posted", lookup_expr="gte"
    )  # on or after
    date_posted__lte = django_filters.DateFilter(
        field_name="date_posted", lookup_expr="lte"
    )  # on or before

    # quota
    quota = django_filters.NumberFilter()  # exact match
    quota_min = django_filters.NumberFilter(
        field_name="quota", lookup_expr="gte"
    )  # greater than or equal to
    quota_max = django_filters.NumberFilter(
        field_name="quota", lookup_expr="lte"
    )  # less than or equal to

    tags = django_filters.CharFilter(lookup_expr="icontains")

    visibility = django_filters.CharFilter(lookup_expr="iexact")
    neighborhood = django_filters.CharFilter(lookup_expr="icontains")
    street_address = django_filters.CharFilter(lookup_expr="icontains")
    city = django_filters.CharFilter(lookup_expr="icontains")
    zip_code = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = ServiceItem
        fields = [
            "title",
            "description",
            "service_provider",
            "date_posted",
            "quota",
            "neighborhood",
            "street_address",
            "city",
            "zip_code",
            "visibility",
            "tags",
        ]
