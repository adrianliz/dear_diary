from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from diary.forms import RegisterForm, MoodForm
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('diary:landing'))


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'diary/dashboard.html'
    context_object_name = 'moods'

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)[:10]


class DeleteMoodView(LoginRequiredMixin, DeleteView):
    model = Mood
    success_url = reverse_lazy('diary:dashboard')


class CreateMoodView(LoginRequiredMixin, CreateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy('diary:dashboard')
    template_name = 'diary/mood.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "New mood"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateMoodView, self).form_valid(form)


class UpdateMoodView(LoginRequiredMixin, UpdateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy('diary:dashboard')
    template_name = 'diary/mood.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "Edit mood"
        return context
