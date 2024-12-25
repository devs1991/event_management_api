import googlemaps
from django.core.mail import send_mail
from django.conf import settings

def send_event_creation_email(organizer, event):
    subject = f"Event Created: {event.title}"
    message = f"Hello {organizer.username},\n\nYou have successfully created the event: {event.title}.\n\nDetails:\n- Location: {event.location}\n- Date: {event.date}\n- Time: {event.time}\n\nThank you for using our platform!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [organizer.email])

def send_event_join_email(attendee, event):
    subject = f"Event Joined: {event.title}"
    message = f"Hello {attendee.username},\n\nYou have successfully joined the event: {event.title}.\n\nDetails:\n- Location: {event.location}\n- Date: {event.date}\n- Time: {event.time}\n\nThank you for using our platform!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [attendee.email])

def get_location_coordinates(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None