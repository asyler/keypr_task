from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from reservations.factories import ReservationFactory
from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ReservationModelViewsetTest(APITestCase):
    list_url_name = 'reservation-list'
    detail_url_name = 'reservation-detail'

    valid_data = {
        'first_name': 'Sten',
        'last_name': 'Kroenke',
        'room_number': '2A',
        'start_date': timezone.now().date(),
        'end_date': (timezone.now() + timezone.timedelta(days=1)).date(),
    }

    invalid_data = {
        'first_name': 'Sten',
        'last_name': 'Kroenke',
        'room_number': '2A',
        'start_date': (timezone.now() + timezone.timedelta(days=1)).date(),
        'end_date': timezone.now().date(),
    }

    def setUp(self):
        ReservationFactory.create()

    def test_smoke_get_returns_json_200(self):
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_return_all_items(self):
        response = self.client.get(reverse(self.list_url_name))

        items = Reservation.objects.all()
        serializer = ReservationSerializer(items, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_valid_single_item(self):
        response = self.client.get(
            reverse(self.detail_url_name, kwargs={'pk': 1}))
        item = Reservation.objects.get(pk=1)

        serializer = ReservationSerializer(item)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_item(self):
        response = self.client.get(
            reverse(self.detail_url_name, kwargs={'pk': 42}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_item(self):
        response = self.client.post(
            reverse('reservation-list'),
            self.valid_data
        )

        item = Reservation.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(item.last_name, 'Kroenke')

    def test_create_invalid_item(self):
        count_before = Reservation.objects.count()

        response = self.client.post(
            reverse('reservation-list'),
            self.invalid_data
        )

        count_after = Reservation.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count_after, count_before)

    def test_valid_update_item(self):
        response = self.client.put(
            reverse(self.detail_url_name, kwargs={'pk': 1}),
            self.valid_data
        )

        item = Reservation.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(item.last_name, 'Kroenke')

    def test_invalid_update_item(self):
        original_last_name = Reservation.objects.get(pk=1).last_name

        response = self.client.put(
            reverse(self.detail_url_name, kwargs={'pk': 1}),
            self.invalid_data
        )

        new_last_name = Reservation.objects.get(pk=1).last_name
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(original_last_name, new_last_name)

    def test_delete_valid_item(self):
        count_before = Reservation.objects.count()

        response = self.client.delete(reverse(self.detail_url_name, kwargs={'pk': 1}))

        count_after = Reservation.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(count_after + 1, count_before)

    def test_delete_invalid_item(self):
        count_before = Reservation.objects.count()

        response = self.client.delete(reverse(self.detail_url_name, kwargs={'pk': 42}))

        count_after = Reservation.objects.count()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(count_after, count_before)


class ReservationSearchTest(TestCase):
    # todo replace timezones.now to simple strings
    def setUp(self):
        self.reservation1 = ReservationFactory.create(
            start_date='2017-09-07',
            end_date='2017-09-10'
        )
        self.reservation2 = ReservationFactory.create(
            start_date='2017-09-08',
            end_date='2017-09-12'
        )

    def test_search_reservations_by_date_range(self):
        response = self.client.get(
            reverse('reservation-list'),
            {
                'start_date_range': '2017-09-10',
                'end_date_range': '2017-09-12'
            }
        )

        serializer = ReservationSerializer([self.reservation1, self.reservation2], many=True)
        self.assertEqual(serializer.data, response.data)

    def test_search_reservations_by_invalid_date_range(self):
        response = self.client.get(
            reverse('reservation-list'),
            {
                'start_date_range': '2017-09-13',
                'end_date_range': '2017-09-06'
            }
        )

        self.assertEqual([], response.data)
