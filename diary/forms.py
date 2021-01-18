from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Mood, Profile


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
            'score': forms.TextInput(attrs={'class': 'form-control-range', 'type': 'range',
                                            'min': 1, 'max': 5})
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'address', 'gender']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'birth_date': forms.DateInput(format=('%Y-%m-%d'),
                                          attrs={'class': 'form-control',
                                                 'type': 'date'
                                                 })
        }
