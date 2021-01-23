from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import Mood, Profile, ContactMessage


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MoodForm(ModelForm):
    class Meta:
        model = Mood
        fields = ['name', 'description', 'score']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'score': forms.TextInput(attrs={'class': 'custom-range', 'type': 'range',
                                            'min': 1, 'max': 5})
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'address', 'gender', 'public']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'birth_date': forms.DateInput(format=('%Y-%m-%d'),
                                          attrs={'class': 'form-control',
                                                 'type': 'date'
                                                 })
        }


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def send_email(self):
        send_mail(
            "New message from user '" + str(self.instance.user) + "'",
            "Subject: '" + self.cleaned_data['subject'] + "'\n" +
            "Message:\n" + self.cleaned_data['message'] + "\n",
            settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
