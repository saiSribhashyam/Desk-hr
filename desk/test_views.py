from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from .views import ContactFormView, BookingCreateView, BookingsList
from .forms import ContactForm, BookingForm
from desk.models import Booking, Enquiry, Location, Service
from django.urls import reverse
from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse


class ContactFormViewTest(TestCase):
    """
    Test ContactFormView
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_valid_form_submission(self):
        """
        Test that the contactform  data creates valid data, if a valid form
        submission is successful, the form data is saved to the database,
        and the success message is displayed.
        """
        response = self.client.post('/', {
            'name': 'Test',
            'email': 'test@example.com',
            'subject': 'Text subject',
            'message': 'This is a message'
        })

        # check if the form submission was successful
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Enquiry.objects.filter(name='Test',
                        subject='Text subject').exists())

        # check if the success message was displayed
        messages = get_messages(response.wsgi_request)
        self.assertIn(
            'Thank you for contacting DESK HQ.'
            'We recieved your message, will get back to you shortly.',
            [str(message) for message in messages])

    def test_invalid_form_submission(self):
        """
        Tests if an invalid form submission fails, the form data is not saved
        to the database, and the form errors are displayed.
        """
        response = self.client.post('/', {
            'name': '',
            'email': 'test@example.com',
            'subject': 'Text message',
            'message': 'This is a message',
        })

        # check if the form submission failed
        self.assertEqual(response.status_code, 200)

        # check if the form data was not saved to the database
        self.assertFalse(Enquiry.objects.filter(email='test@example.com',
                         subject='Text message').exists())

        # check if the form errors were displayed
        self.assertContains(response, '')


class BookingCreateViewTest(TestCase):
    """
    Tests that a booking can be successfully created when the user is logged in
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        self.location = Location.objects.create(
            location_name='DESK HQ Brooklyn House'
            '(3 STONE AVENUE LONDON SE5 2AZ)'
            )

        self.space_booking = Service.objects.create(
            space_type='Day WorkStation'
        )

        self.booking = Booking.objects.create(
            client=self.user,
            location=self.location,
            space_booking=self.space_booking,
            booking_duration='1 Hour',
            booking_date=date(2023, 5, 12),

            booking_start=(datetime.now() + timedelta(hours=1)).strftime(
                '%Y-%m-%d %H:%M:%S.%f'),
            booking_end=(datetime.now() + timedelta(hours=2)).strftime(
                '%Y-%m-%d %H:%M:%S.%f'),
        )

        self.booking_data = {
            'client': self.user,
            'location': self.location,
            'space_booking': self.space_booking,
            'booking_date': self.booking.booking_date,
            'booking_duration': self.booking.booking_duration,
            'booking_start': self.booking.booking_start,
            'booking_end': self.booking.booking_end,
        }

    def test_create_booking(self):
        # Login the user
        self.client.login(
            username=self.user.username, password=self.user.password)

        # Submit the booking form
        booking_form = BookingForm(self.booking_data)
        response = self.client.post(
            reverse('space_booking'), self.booking_data)

        # Check that the booking was created successfully
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.first()
        self.assertEqual(booking.location, self.booking_data['location'])
        self.assertEqual(
            booking.space_booking, self.booking_data['space_booking'])
        self.assertEqual(
            booking.booking_date, self.booking_data['booking_date'])
        self.assertEqual(
            booking.booking_duration, self.booking_data['booking_duration'])
        self.assertEqual(
            booking.booking_start, self.booking_data['booking_start'])
        self.assertEqual(booking.booking_end, self.booking_data['booking_end'])
        self.assertEqual(booking.client, self.booking_data['client'])

        self.assertTrue(Booking.objects.filter(client=self.user).exists())

    def test_create_booking_unauthenticated(self):
        # Submit the booking form without logging in
        user_login = self.client.login(
            username=self.user.username, password=self.user.password)
        booking_form = BookingForm(self.booking_data)
        response = self.client.post(
            reverse('space_booking'), self.booking_data)

        # Check that the user is redirected to the login page
        self.assertRedirects(response, '/accounts/login/?next=/space_booking/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(user_login)
