from django.urls import path
from diary.views import LandingView, SingupView, DashboardView, \
    DeleteMoodView, CreateMoodView, EditMoodView, ProfileView, EditProfileView, logout_view

app_name = 'diary'
urlpatterns = [
    path('', LandingView.as_view(), name="landing"),
    path('singup/', SingupView.as_view(), name="singup"),
    path('logout/', logout_view, name="logout"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('delete/<int:pk>/', DeleteMoodView.as_view(), name="delete"),
    path('create/', CreateMoodView.as_view(), name="create"),
    path('edit/<int:pk>/', EditMoodView.as_view(), name="edit"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/edit/<int:pk>', EditProfileView.as_view(), name="edit_profile")
]
