from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, success_subscription, cancel_subscription, create_subscription

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('verify_message/', TemplateView.as_view(template_name='users/verify_message.html'), name='verify_message'),
    path('success_profile/', TemplateView.as_view(template_name='users/success_profile.html'), name='success_profile'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('cancel/', cancel_subscription, name='cancel_subscription'),
    path('success/', success_subscription, name='success_subscription'),

    path('subscription/create/', create_subscription, name='subscription_create'),

]
