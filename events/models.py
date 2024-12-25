from django.db import models
from users.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    max_attendees = models.PositiveIntegerField()
    organizer = models.ForeignKey(User, related_name='organized_events', on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='joined_events', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'location', 'organizer'], name='unique_event_for_organizer'),
        ]