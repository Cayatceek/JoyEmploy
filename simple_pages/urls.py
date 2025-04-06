from django.urls import path
from . import views
from .views import dashboard, custom_logout, aboutus, news
from django.contrib.auth.views import LoginView
from employees.forms import EmployeeAuthenticationForm

urlpatterns = [
    path("login/", LoginView.as_view(
        template_name="auth/login.html",
        authentication_form=EmployeeAuthenticationForm
    ), name="login"),
    path("login/", LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", custom_logout, name='logout'),
    path('', views.home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('about/', aboutus, name='about'),
    path('news/', news, name= 'news'),

]
