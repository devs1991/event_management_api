from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOrganizerOrAdmin
from .utils import send_event_creation_email, send_event_join_email
from .utils import get_location_coordinates

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsOrganizerOrAdmin()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if "attendees" in request.data:
            for attendee_id in request.data["attendees"]:
                attendee = instance.attendees.filter(id=attendee_id).first()
                if attendee:
                    send_event_join_email(attendee, instance)
        return super().update(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        event = serializer.save()
        lat, lng = get_location_coordinates(event.location)
        if lat and lng:
            event.latitude = lat
            event.longitude = lng
            event.save()
        send_event_creation_email(event.organizer, event)