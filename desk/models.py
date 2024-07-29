from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError


class Enquiry(models.Model):
    """
    Model for contact enquiries.
    """
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=80)
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for ordering the queryset by the 'date'
        field in descending order.
        """
        ordering = ["-date"]

    def __str__(self):
        """
        String representation of Contact Form message.
        """
        return f"from {self.name} | subject: {self.subject}"


VALID = 0
CANCELLED = 1
STATUS = [
    (VALID, "Valid"), (CANCELLED, "Cancelled")
]

# Office space locations
OFFICE_LOCATION = [
    ('DESK HQ Brooklyn House (3 STONE AVENUE LONDON SE5 2AZ)',
        'DESK HQ Brooklyn House (3 STONE AVENUE LONDON SE5 2AZ)'),
    ('DESK HQ Dockyard Place (55 PARADE STREET LONDON E20 3YB)',
        'DESK HQ Dockyard Place (55 PARADE STREET LONDON E20 3YB)'),
]

# Create field choices for Services Offered
SERVICES = [
    ('Seat1', 'S1'),
('Seat2', 'S2'),
('Seat3', 'S3'),
('Seat4', 'S4'),
('Seat5', 'S5'),
('Seat6', 'S6'),
('Seat7', 'S7'),
('Seat8', 'S8'),
('Seat9', 'S9'),
('Seat10', 'S10'),
('Seat11', 'S11'),
('Seat12', 'S12'),
('Seat13', 'S13'),
('Seat14', 'S14'),
('Seat15', 'S15'),
('Seat16', 'S16'),
('Seat17', 'S17'),
('Seat18', 'S18'),
('Seat19', 'S19'),
('Seat20', 'S20')
,
]

# Duration
DURATION = [
    ('1 Hour', '1 Hour'),
    ('2 Hours', '2 Hours'),
    ('3 Hours', '3 Hours'),
    ('4 Hours', '4 Hours'),
    ('5 Hours', '5 Hours'),
    ('6 Hours', '6 Hours'),
    ('7 Hours', '7 Hours'),
    ('8 Hours', '8 Hours'),
    ('All day', 'All day'),
]


# Booking Times
HOURS = [
    ("09:00 am", "09:00 am"),
    ("09:30 am", "09:30 am"),
    ("10:00 am", "10:00 am"),
    ("10:30 am", "10:30 am"),
    ("11:00 am", "11:00 am"),
    ("11:30 am", "11:30 am"),
    ("12:00 pm", "12:00 pm"),
    ("12:30 pm", "12:30 pm"),
    ("13:00 pm", "13:00 pm"),
    ("13:30 pm", "13:30 pm"),
    ("14:00 pm", "14:00 pm"),
    ("14:30 pm", "14:30 pm"),
    ("15:00 pm", "15:00 pm"),
    ("15:30 pm", "15:30 pm"),
    ("16:00 pm", "16:00 pm"),
    ("16:30 pm", "16:30 pm"),
    ("17:00 pm", "17:00 pm"),
    ("17:30 pm", "17:30 pm"),
]


def validate_date(date):
    """
    Create validation for user chosen date
    """
    if date <= timezone.now().date():
        raise ValidationError("Date cannot be in the past or the same day.")
    return date


class Location(models.Model):
    """
    Create entry for specific workspace and location
    """
    location_id = models.IntegerField(primary_key=True, default=1)
    location_name = models.CharField(
        max_length=200,
        choices=OFFICE_LOCATION,
        default="DESK HQ Brooklyn House (3 STONE AVENUE LONDON SU5 2AZ)")

    slug = models.SlugField(max_length=200, unique=True)
    featured_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        """
        String representation of Booking location.
        """
        return self.location_name


class Service(models.Model):
    """
    Create entry for specific workspace service type
    """
    space_type = models.CharField(
        max_length=50, choices=SERVICES,
        unique=True, default='Day WorkStation')
    content = models.TextField(blank=True)
    featured_image = CloudinaryField('image', default='placeholder')
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        """
        String representation of Booking Service by space type.
        """
        return f"{self.space_type}"


class Booking(models.Model):
    """
    Create entry for Customer booking system
    """
    client = models.ForeignKey(
        User, on_delete=models.CASCADE)

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE, null=True,
        default="DESK HQ Brooklyn House (3 STONE AVENUE LONDON SE5 2AZ)")

    space_booking = models.ForeignKey(
        Service,
        on_delete=models.CASCADE, related_name='space_bookings',
        null=True, default="Day WorkStation")

    booking_date = models.DateField(
        default=(timezone.now().date() + timezone.timedelta(days=1)),
        validators=[validate_date])
    booking_duration = models.CharField(
        max_length=20,
        choices=DURATION,
        default="Anytime")

    booking_start = models.CharField(
        max_length=20,
        choices=HOURS,
        default="09:00 am")

    booking_end = models.CharField(
        max_length=20,
        choices=HOURS,
        default="09:00 am")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=1)
    approved = models.BooleanField(default=False)

    class Meta:
        """
        Meta class for ordering the queryset by the 'created_on'
        field in descending order.
        """
        unique_together = [
            'location', 'space_booking', 'booking_date',
            'booking_start', 'booking_end']
        ordering = ['-created_on']

    def __str__(self):
        """
        String representation of Booking object.
        """
        return "{} booked {} | {} | {} | {}".format(
            self.client, self.space_booking, self.booking_date,
            self.booking_start, self.booking_end)
