from django.urls import path
from diary.views import LandingView, SingupView, DashboardView, \
    DeleteMoodView, CreateMoodView, UpdateMoodView, logout_view

app_name = 'diary'
urlpatterns = [
    path('', LandingView.as_view(), name="landing"),
    path('singup/', SingupView.as_view(), name="singup"),
    path('logout/', logout_view, name="logout"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('delete/<int:pk>/', DeleteMoodView.as_view(), name="delete"),
    path('create/', CreateMoodView.as_view(), name="create"),
    path('edit/<int:pk>/', UpdateMoodView.as_view(), name="edit")
]
