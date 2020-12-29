from django.shortcuts import render, reverse
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from diary.forms import RegisterForm
from django.http import HttpResponseRedirect
from .models import Mood

class LandingView(View):
    form_class = AuthenticationForm
    template_name = 'diary/landing.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'form_name': 'Login'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(None, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('diary:dashboard'))

        return render(request, self.template_name, {'form': form, 'form_name': 'Login'})

class SingupView(View):
    form_class = RegisterForm
    template_name = 'diary/singup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'form_name': 'Sing up'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if (form.is_valid()):
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('diary:dashboard'))

        return render(request, self.template_name, {'form': form, 'form_name': 'Sing up'})

class DashboardView(LoginRequiredMixin, ListView):
    login_url = '/'
    template_name='diary/dashboard.html'
    context_object_name='moods'

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)[:10]
