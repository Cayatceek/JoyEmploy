from django.urls import path
from . import views
from .views import custom_logout, aboutus, custom_login_view
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("login/", custom_login_view, name="login"),
    path("login/", LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", custom_logout, name='logout'),
    path('', views.home, name='home'),
    path('about/', aboutus, name='about'),
]
