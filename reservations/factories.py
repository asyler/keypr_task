import factory

from reservations.models import Reservation


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    room_number = factory.Faker('secondary_address')
    start_date = factory.Faker('past_date')
    end_date = factory.Faker('future_date')
