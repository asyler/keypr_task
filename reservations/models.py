from django.core.exceptions import ValidationError
from django.db import models

def validate_end_datetime(value):
    pass

# Create your models here.
class Reservation(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(validators=[validate_end_datetime])

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('End date should be after start date')
