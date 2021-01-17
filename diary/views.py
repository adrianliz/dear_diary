from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from diary.forms import RegisterForm, MoodForm, ProfileForm
from django.http import HttpResponseRedirect

from .models import Mood, Profile


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


class SingupView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('diary:dashboard')
    template_name = 'diary/core/page_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "Sing up"
        context['page_title'] = "Welcome to DearDiary"
        context['back_url'] = reverse('diary:landing')
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse('diary:dashboard'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('diary:landing'))


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'diary/dashboard.html'
    context_object_name = 'moods'
    paginate_by = 5

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user).order_by('-updated_on')


class CreateMoodView(LoginRequiredMixin, CreateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy('diary:dashboard')
    template_name = 'diary/core/page_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "New mood"
        context['include_navbar'] = True
        context['page_title'] = "How it's going? <i class=\"ml-2 far fa-lightbulb\"></i>"
        context['back_url'] = reverse('diary:dashboard')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateMoodView, self).form_valid(form)


class OwnershipValidator(UserPassesTestMixin):
    def test_func(self):
        self.object = self.get_object()
        return self.request.user == self.object.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('diary:dashboard'))


class DeleteMoodView(LoginRequiredMixin, OwnershipValidator, DeleteView):
    model = Mood
    success_url = reverse_lazy('diary:dashboard')


class EditMoodView(LoginRequiredMixin, OwnershipValidator, UpdateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy('diary:dashboard')
    template_name = 'diary/core/page_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "Edit mood"
        context['include_navbar'] = True
        context['page_title'] = "How it's going? <i class=\"ml-2 far fa-lightbulb\"></i>"
        context['back_url'] = reverse('diary:dashboard')
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'diary/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        profile = Profile.objects.get_or_create(user=self.request.user)[0]
        context['profile'] = profile
        return context


class EditProfileView(LoginRequiredMixin, OwnershipValidator, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('diary:profile')
    template_name = 'diary/core/page_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "Edit profile"
        context['include_navbar'] = True
        context['back_url'] = reverse('diary:profile')
        return context
