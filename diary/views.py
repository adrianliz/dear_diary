from django.shortcuts import render
from django.views.generic.base import TemplateView
from diary.forms import RegisterForm


class LandingView(TemplateView):
    template_name = "diary/index.html"


def register(request):
    form = RegisterForm()

    if (request.method == 'POST'):
        form = RegisterForm(request.POST)

        if (form.is_valid()):
            form.save()

    context = {'form': form}
    return render(request, 'diary/register.html', context)
