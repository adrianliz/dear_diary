from django.urls import path
from diary.views import LandingView, register

app_name = 'diary'
urlpatterns = [
    path('', LandingView.as_view(), name="landing"),
    path('register', register, name="register")
]
