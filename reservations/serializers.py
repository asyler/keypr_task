import serializers
from rest_framework import serializers

from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'first_name', 'last_name', 'room_number', 'start_date', 'end_date')

    def validate(self, attrs):
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError({'end_date': 'End date should be after start date'})
        return attrs
