from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='attendee')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email'),
            models.UniqueConstraint(fields=['username'], name='unique_username'),
        ]