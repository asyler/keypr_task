# Create your views here.
from rest_framework import viewsets, filters

from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class DateRangeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'start_date_range' in request.GET and 'end_date_range' in request.GET:
            return queryset.filter(
                start_date__lte=request.GET['end_date_range'],
                end_date__gte=request.GET['start_date_range']
            )
        return queryset


class ReservationsView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = (DateRangeFilter,)
