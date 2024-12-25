from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_max_attendees(self, value):
        """Ensure max_attendees is a positive integer."""
        if value <= 0:
            raise serializers.ValidationError("Maximum attendees must be greater than zero.")
        return value

    def validate_date(self, value):
        """Ensure the event date is in the future."""
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("The event date must be in the future.")
        return value

    def validate(self, data):
        """Ensure the location and title are unique for the organizer."""
        title = data.get('title')
        location = data.get('location')
        organizer = data.get('organizer')
        if Event.objects.filter(title=title, location=location, organizer=organizer).exists():
            raise serializers.ValidationError("An event with this title and location already exists for this organizer.")
        return data
