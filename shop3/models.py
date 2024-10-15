from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta


class Studio(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=255)   
    photo = models.ImageField(upload_to='studios/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default='Default Address', editable=False)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guests = models.IntegerField()

    def save(self, *args, **kwargs):
        # Automatically set the studio address from the related Studio instance
        self.address = self.studio.address
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.studio.name} on {self.date} from {self.start_time} to {self.end_time}"

class TimeSlot(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    @staticmethod
    def create_time_slots(studio, date):
        current_time = datetime.strptime('10:00', '%H:%M').time()
        end_time = datetime.strptime('19:00', '%H:%M').time()

        while current_time < end_time:
            next_time = (datetime.combine(date, current_time) + timedelta(hours=3)).time()
            is_available = True

            bookings = Booking.objects.filter(studio=studio, date=date, start_time__lt=next_time, end_time__gt=current_time)
            total_guests = sum(booking.guests for booking in bookings)

            if total_guests >= studio.capacity:
                is_available = False

            TimeSlot.objects.create(
                studio=studio,
                date=date,
                start_time=current_time,
                end_time=next_time,
                is_available=is_available
            )

            current_time = (datetime.combine(date, current_time) + timedelta(hours=1)).time()

    def __str__(self):
        return f"TimeSlot for {self.studio.name} on {self.date} from {self.start_time} to {self.end_time}"


