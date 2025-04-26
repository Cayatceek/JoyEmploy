from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employees.models import Employee
from .forms import EmployeeRegistrationForm
from django.db import IntegrityError
from django.http import JsonResponse

# Декоратор для проверки роли HR или Superadmin
def hr_or_superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'hr'):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "У вас нет прав для доступа к этой странице.")
            return redirect('home')  # Или другая страница, куда перенаправлять
    return wrapper

@login_required
@hr_or_superadmin_required
def manage_panel(request):
    """Панель управления сотрудниками"""
    employees = Employee.objects.all()
    return render(request, "manage_panel/manage_panel.html", {"employees": employees})

@login_required
@hr_or_superadmin_required
def register_employee(request):
    """HR или администратор могут зарегистрировать нового сотрудника"""
    if request.method == "POST":
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            try:
                employee = form.save()
                messages.success(request, f"Сотрудник {employee.name} успешно зарегистрирован.")
                return redirect("manage_panel")
            except IntegrityError:
                form.add_error('email', "Этот email уже используется. Выберите другой.")
            except Exception as e:
                messages.error(request, f"Ошибка при регистрации: {str(e)}")
    else:
        form = EmployeeRegistrationForm()

    return render(request, "manage_panel/register_employee.html", {"form": form})

@login_required
@hr_or_superadmin_required
def delete_employee(request, employee_id):
    """Удаление сотрудника HR или суперадмином"""
    employee = get_object_or_404(Employee, id=employee_id)

    # Проверяем, что пользователь не пытается удалить самого себя
    if request.user.id == employee.id:
        return JsonResponse({"success": False, "message": "Вы не можете удалить самого себя."}, status=403)

    try:
        employee.delete()
        return JsonResponse({"success": True, "message": f"Сотрудник {employee.name} успешно удалён."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@login_required
@hr_or_superadmin_required
def employee_list(request):
    """Список всех сотрудников"""
    employees = Employee.objects.all()
    return render(request, "manage_panel/employee_list.html", {"employees": employees})

@login_required
@hr_or_superadmin_required
def edit_employee(request, employee_id):
    """Редактирование сотрудника HR или суперадмином"""
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        form = EmployeeRegistrationForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Данные сотрудника {employee.name} успешно обновлены.")
            return redirect("manage_panel")
        else:
            print(form.errors)  # Для отладки
    else:
        form = EmployeeRegistrationForm(instance=employee)

    return render(request, "manage_panel/edit_employee.html", {"form": form, "employee": employee})