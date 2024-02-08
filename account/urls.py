from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserTaskAccountUpdateView, ProfileData, edit_profile, pass_change

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileData, name='profile'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('profile/edit/pass_change/', pass_change, name='pass_change'),
]

