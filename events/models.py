from django.db import models
import uuid


class Event(models.Model):
    title = models.CharField(max_length=150)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    thumbnail = models.ImageField(upload_to='events/')

    def __str__(self):
        return self.title


class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    reservation_code = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)


class Ticket(models.Model):
    buyer = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reservation_code = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'Your Reservation Code for {self.event} is {self.reservation_code}'
