from django import forms
from accounts.models import GuestEmail


class ContactForm(forms.ModelForm):
    class Meta:
        model = GuestEmail
        fields = ('full_name', 'email', 'phone', 'reason')
