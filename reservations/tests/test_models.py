from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from reservations.models import Reservation

class ReservationModelTest(TestCase):
    def test_start_date_cannot_be_empty(self):
        reservation = Reservation()
        with self.assertRaises(ValidationError):
            Reservation._meta.get_field('start_date').clean(reservation.start_date, reservation)

    def test_end_date_cannot_be_empty(self):
        reservation = Reservation()
        with self.assertRaises(ValidationError):
            Reservation._meta.get_field('end_date').clean(reservation.end_date, reservation)


    def test_start_date_should_be_before_end_date(self):
        reservation = Reservation(
            start_date = timezone.now(),
            end_date = timezone.now()-timezone.timedelta(minutes=1)
        )
        with self.assertRaises(ValidationError):
            reservation.save()
            reservation.full_clean()