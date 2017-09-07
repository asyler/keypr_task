from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Reservation(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    room_number = models.CharField(max_length=256)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # todo: make date not datetime

    # todo: move validation to serializer
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('End date should be after start date')
