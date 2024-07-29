from django.test import TestCase
from datetime import date
from .models import Booking, Enquiry, Location, Service
from django.contrib.auth.models import User


class BookingTest(TestCase):
    """
    Test user booking
    """

    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            password='testpasswd')

        self.location = Location.objects.create(
            location_name='DESK HQ Brooklyn House'
            '(3 STONE AVENUE LONDON SE5 2AZ)')

        self.space_booking = Service.objects.create(
            space_type='Day WorkStation')

        self.booking = Booking.objects.create(
            client=self.user,
            location=self.location,
            space_booking=self.space_booking,
            booking_date=date(2023, 4, 8),
            booking_start='09:00 am',
            booking_end='10:00 am'
            )

    def test_booking_str(self):
        """
        Test string representation of the booking
        """
        client_booking = str(self.booking.client)
        location_booking = str(self.booking.location)
        space_booking = str(self.booking.space_booking)
        booking_date = str(self.booking.booking_date)
        booking_start = str(self.booking.booking_start)
        booking_end = str(self.booking.booking_end)

        self.assertEqual(
            str(self.booking),
            "{} booked {} | {} | {} | {}".format(
                client_booking, space_booking,
                booking_date, booking_start, booking_end))


class EnquiryTest(TestCase):

    def setUp(self):
        self.enquiry = Enquiry.objects.create(
            name='john',
            subject='text')

    def test_enquiry_str(self):
        """
        Test user inquiry contact form object present a string
        """
        enquiry_name = str(self.enquiry.name)
        enquiry_subject = str(self.enquiry.subject)
        self.assertEqual(
            str(self.enquiry),
            f"from {enquiry_name} | subject: {enquiry_subject}")


class LocationTest(TestCase):
    def setUp(self):
        self.location1 = Location.objects.create(
            location_name='DESK HQ Brooklyn House'
            '(3 STONE AVENUE LONDON SE5 2AZ)')

    def test_location_name_str(self):
        """
        Test string representation of the location_name
        """
        loc = str(self.location1.location_name)
        self.assertEqual(str(self.location1), (loc))


class ServiceTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            space_type='Day WorkStation')

    def test_space_type_str(self):
        """
        Test string representation of the space_type
        """
        service_type = str(self.service.space_type)
        self.assertEqual(str(self.service), f"{service_type}")
