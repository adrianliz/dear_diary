from django.urls import path
from diary.views import LandingView, SingupView, dashboard

app_name = 'diary'
urlpatterns = [
    path('', LandingView.as_view(), name="landing"),
    path('singup/', SingupView.as_view(), name="singup"),
    path('dashboard/', dashboard, name="dashboard")
]
