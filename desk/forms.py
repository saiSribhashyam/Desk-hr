from django import forms
from .models import Booking, Enquiry


class BookingForm(forms.ModelForm):
    """
    Create BookingForm
    """
    class Meta:
        model = Booking
        fields = [
            'location', 'space_booking', 'booking_date',
            'booking_duration', 'booking_start', 'booking_end']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ContactForm(forms.ModelForm):
    """
    User model contact for enquires.
    """
    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'kerry@example.com.'}))
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Enquiry
        fields = [
            'name', 'email', 'subject', 'message'
            ]
