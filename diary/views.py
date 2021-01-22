from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, TemplateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg

from .models import Mood, Profile
from .forms import RegisterForm, MoodForm, ProfileForm, ContactForm


class UserNotLoggedValidator(UserPassesTestMixin):
    def test_func(self):
        # Únicamente cuando el usuario NO esté autenticado
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('diary:dashboard'))


class LandingView(UserNotLoggedValidator, View):
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


class SignupView(UserNotLoggedValidator, CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('diary:dashboard')
    template_name = 'diary/core/page_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "Sign up"
        context['page_title'] = "Welcome! <i class=\"skin-color fas fa-hand-sparkles\"></i>"
        context['back_url'] = reverse('diary:landing')
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse('diary:dashboard'))


@login_required()
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
        context['page_title'] = "How it's going? <i class=\"ml-2 far fa-lightbulb text-warning\"></i>"
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
        context['page_title'] = "How it's going? <i class=\"ml-2 far fa-lightbulb text-warning\"></i>"
        context['back_url'] = reverse('diary:dashboard')
        return context

    def form_valid(self, form):
        mood = form.save(commit=False)
        mood.updated_on = timezone.now()
        mood.save()
        return super(EditMoodView, self).form_valid(form)


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


class ContactView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ContactForm
    template_name = 'diary/core/page_form.html'
    success_message = 'Message sent correctly'
    success_url = reverse_lazy('diary:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "Contact"
        context['include_navbar'] = True
        context['back_url'] = reverse('diary:dashboard')
        return context

    def form_valid(self, form):
        contact_message = form.save(commit=False)
        contact_message.user = self.request.user
        contact_message.save()
        form.send_email()
        return super().form_valid(form)


class EvolutionView(LoginRequiredMixin, TemplateView):
    template_name = 'diary/evolution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg_scores'] = Mood.objects.filter(
            user=self.request.user).values('updated_on__date').annotate(avg=Avg('score'))
        return context
