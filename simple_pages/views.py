import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

from employees.forms import EmployeeAuthenticationForm

logger = logging.getLogger(__name__)

def home(request):
    return render(request, "home.html")


def aboutus(request):
    return render(request, "about.html")


def custom_logout(request):
    logout(request)
    return render(request, "auth/logout.html")

def custom_login_view(request):
    # Если пользователь уже аутентифицирован, перенаправляем на панель управления
    if request.user.is_authenticated:
        return redirect('manage_panel')

    if request.method == "POST":
        form = EmployeeAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Используем email как username
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {user.name}!")
                return redirect('manage_panel')
            else:
                messages.error(request, "Неверный email или пароль.")
        else:
            messages.error(request, "Ошибка в данных формы. Проверьте email и пароль.")
    else:
        form = EmployeeAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})