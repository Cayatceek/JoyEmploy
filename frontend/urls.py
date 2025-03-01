from django.urls import path
from . import views
from .views import dashboard, custom_logout
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", custom_logout, name='logout'),
    path('', views.home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
]
