from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from reservations.models import Reservation


class ReservationModelTest(TestCase):
    def _test_field_cannot_be_empty(self, field_name):
        reservation = Reservation()
        with self.assertRaises(ValidationError):
            Reservation._meta.get_field(field_name).clean(getattr(reservation, field_name), reservation)

    def test_fields_cannot_be_empty(self):
        self._test_field_cannot_be_empty('start_date')
        self._test_field_cannot_be_empty('end_date')
        self._test_field_cannot_be_empty('first_name')
        self._test_field_cannot_be_empty('last_name')
        self._test_field_cannot_be_empty('room')

    def test_start_date_should_be_before_end_date(self):
        reservation = Reservation(
            start_date=timezone.now(),
            end_date=timezone.now() - timezone.timedelta(minutes=1)
        )
        with self.assertRaises(ValidationError):
            reservation.save()
            reservation.full_clean()
