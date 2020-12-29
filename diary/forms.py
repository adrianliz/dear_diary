from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Mood

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
                                      'min': 1, 'max': 5})}

