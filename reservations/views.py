from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ReservationsView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer