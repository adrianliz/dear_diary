from django.shortcuts import render, reverse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from diary.forms import RegisterForm
from django.http import HttpResponseRedirect

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
            form.save()
            return HttpResponseRedirect(reverse('diary:dashboard'))

        return render(request, self.template_name, {'form': form, 'form_name': 'Sing up'})

def dashboard(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'diary/dashboard.html', {'username': user.username})
    else:
        return HttpResponseRedirect(reverse('diary:dashboard'))
