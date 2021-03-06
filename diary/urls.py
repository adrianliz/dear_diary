from django.urls import path
from diary.views import LandingView, SignupView, DashboardView, \
    DeleteMoodView, CreateMoodView, EditMoodView, ProfileView, \
    EditProfileView, ContactView, EvolutionView, CommunityView, \
    RankingView, CommunityUserView, AdvicesView, logout_view

app_name = 'diary'
urlpatterns = [
    path('', LandingView.as_view(), name="landing"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('logout/', logout_view, name="logout"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('delete/<int:pk>/', DeleteMoodView.as_view(), name="delete"),
    path('create/', CreateMoodView.as_view(), name="create"),
    path('edit/<int:pk>/', EditMoodView.as_view(), name="edit_mood"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/edit/<int:pk>', EditProfileView.as_view(), name="edit_profile"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('evolution/', EvolutionView.as_view(), name="evolution"),
    path('community/', CommunityView.as_view(), name="community"),
    path('ranking/', RankingView.as_view(), name="ranking"),
    path('community/<int:pk>', CommunityUserView.as_view(), name="community_user"),
    path('advices/', AdvicesView.as_view(), name="advices")
]
