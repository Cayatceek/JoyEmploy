from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employees.models import Employee, Task

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    try:
        employee = Employee.objects.get(user=request.user)  # Ищем сотрудника, связанного с User
    except Employee.DoesNotExist:
        return render(request, "no_access.html")  # Если нет, доступ запрещён

    # Проверяем, есть ли у сотрудника роль
    if not employee.role or employee.role.name not in ["hr", "superadmin"]:  
        return render(request, "no_access.html")

    employees = Employee.objects.all()
    tasks = Task.objects.all()
    return render(request, "dashboard.html", {"employees": employees, "tasks": tasks})

from django.contrib.auth import logout
from django.shortcuts import redirect, render

def custom_logout(request):
    logout(request)  # Выход пользователя
    return render(request, 'logout.html')  # Отображение кастомной страницы
