from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.html import escape
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, TemplateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count, Sum

from .models import Mood, Profile, Advice
from .forms import RegisterForm, MoodForm, ProfileForm, ContactForm


class UserNotLoggedValidator(UserPassesTestMixin):
    def test_func(self):
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
    template_name = 'diary/core/page-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "Sign up"
        context['page_title'] = "Welcome! <i class=\"skin-color fas fa-hand-sparkles\"></i>"
        context['back_url'] = reverse('diary:landing')
        return context

    def form_valid(self, form):
        login(self.request, form.save())
        return HttpResponseRedirect(reverse('diary:dashboard'))


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('diary:landing'))


def validate_sortby(sortby):
    if (sortby != 'name' and sortby != '-score'):
        return '-updated_on'
    else:
        return sortby


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'diary/dashboard.html'
    context_object_name = 'moods'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allow_crud'] = True
        context['username'] = self.request.user
        return context

    def get_queryset(self):
        sortby = validate_sortby(escape(self.request.GET.get('sortby')))
        return Mood.objects.filter(user=self.request.user).order_by(sortby)


class CreateMoodView(LoginRequiredMixin, CreateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy('diary:dashboard')
    template_name = 'diary/core/page-form.html'

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
    template_name = 'diary/core/page-form.html'

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
        context['profile'] = Profile.objects.get_or_create(
            user=self.request.user)[0]
        return context


class EditProfileView(LoginRequiredMixin, OwnershipValidator, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('diary:profile')
    template_name = 'diary/core/page-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "Edit profile"
        context['include_navbar'] = True
        context['back_url'] = reverse('diary:profile')
        return context


class ContactView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ContactForm
    template_name = 'diary/core/page-form.html'
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


class CommunityView(LoginRequiredMixin, ListView):
    template_name = 'diary/community.html'
    context_object_name = 'profiles'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Only users with public profile
        target_users = Profile.objects.exclude(
            user=self.request.user).filter(public=True).values('user')
        context['moods_count'] = Mood.objects.filter(user__in=target_users).values('user').annotate(
            count=Count('user'))
        return context

    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user).order_by('user')


class CommunityUserView(LoginRequiredMixin, ListView):
    template_name = 'diary/dashboard.html'
    context_object_name = 'moods'
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=self.kwargs['pk'])[0]
        # Dispatch if profile is private or is the same profile
        if (not profile.public) or (profile.user == request.user):
            return HttpResponseRedirect(reverse('diary:community'))
        else:
            return super(CommunityUserView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allow_crud'] = False
        context['username'] = Profile.objects.filter(
            user=self.kwargs['pk'])[0].user
        return context

    def get_queryset(self):
        sortby = validate_sortby(escape(self.request.GET.get('sortby')))
        return Mood.objects.filter(user=self.kwargs['pk']).order_by(sortby)


def validate_ranking(ranking):
    if (ranking != 'moods' and ranking != 'score'):
        return 'moods'
    else:
        return ranking


class RankingView(LoginRequiredMixin, TemplateView):
    template_name = 'diary/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ranking_type"] = validate_ranking(
            escape(self.request.GET.get('ranking')))

        users_moods = Mood.objects.values('user__username')
        if context["ranking_type"] == "moods":
            context["user_ranking"] = users_moods.annotate(
                value=Count('user__username')).order_by('-value')[:10]
        else:
            context["user_ranking"] = users_moods.annotate(
                value=Sum('score')).order_by('-value')[:10]
        return context


class AdvicesView(LoginRequiredMixin, TemplateView):
    template_name = 'diary/advices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advices'] = Advice.objects.values(
            'description', 'likes', 'user__username')

        return context
