from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ReservationModelTest(TestCase):
    def test_start_date_should_be_before_end_date(self):
        reservation = Reservation(
            first_name='Greg',
            last_name='Greggie',
            room_number='28',
            start_date=timezone.now(),
            end_date=timezone.now() - timezone.timedelta(minutes=1)
        )
        serializer = ReservationSerializer(instance=reservation)
        serializer = ReservationSerializer(data=serializer.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('end_date', serializer.errors)

