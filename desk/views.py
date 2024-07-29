from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from desk.models import Booking, Service, Enquiry
from .forms import BookingForm, ContactForm
from django.views.generic.edit import FormView, UpdateView, DeleteView


class HomePageView(TemplateView):
    """
    Views for home page.
    """
    template_name = 'home/index.html'


class ContactFormView(FormView):
    """
    Views for users ContactForm for equiry
    """
    model = Enquiry
    form_class = ContactForm
    template_name = 'home/index.html'

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            contact_form = self.form_class(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(
                    self.request,
                    'Thank you for contacting DESK HQ.'
                    'We recieved your message, will get back to you shortly.')
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.info(
                    self.request,
                    'This field is required')
                return HttpResponse("")


class BookingsList(LoginRequiredMixin, ListView):
    """
    Views for users Booking
    """
    model = Booking
    template_name = 'desk/booking_details.html'
    context_object_name = 'bookings'
    paginate_by = 4

    def get_queryset(self):
        return Booking.objects.filter(client=self.request.user)


class BookingCreateView(LoginRequiredMixin, FormView):
    """
    View for displaying booking form and allow user to create booking,
    when user logged in.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'desk/space_booking.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        # <process form cleaned data>
        form.save()
        messages.success(
            self.request,
            'Thank you for using DESK HQ.'
            'Booking was created successfully. View in Booking Details')
        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        messages.error(
            self.request, 'Sorry, there was an error with your booking.')
        return super().form_invalid(form)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    """
    View allows user to edit and update their booking and
    redirects them to booking details.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'desk/update_booking.html'
    success_url = reverse_lazy('booking_details')

    def get_object(self, queryset=None):
        """
        Retrieve the object to be updated, using the primary key from the URL
        """
        booking = get_object_or_404(Booking, pk=self.kwargs['pk'])
        return booking

    def form_valid(self, form):
        messages.success(self.request, 'Booking updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Booking update failed. Please check the form and try again.')
        return super().form_invalid(form)


class BookingDeleteView(DeleteView):
    """
    Views allow user to delete booking and redirect user to booking details.
    """
    model = Booking
    template_name = 'desk/delete_booking.html'
    success_url = reverse_lazy('booking_details')

    def get_object(self, queryset=None):
        """
        Retrieve the object to be deleted, using the primary key from the URL
        """
        booking_detail = get_object_or_404(Booking, pk=self.kwargs['pk'])
        return booking_detail

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Booking deleted successfully!')
        return super().form_valid(form)


class AboutView(TemplateView):
    """
    View for about_us page
    """
    template_name = 'home/about_us.html'


class ServiceListView(ListView):
    """
    View for services page
    """
    template_name = 'home/services.html'
    queryset = Service.objects.order_by('-timestamp')
    context_object_name = 'services'
