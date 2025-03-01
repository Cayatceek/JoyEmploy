from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from employees.models import Employee, Role
from .forms import EmployeeRegistrationForm

@login_required
def register_employee(request):
    if not request.user.employee.role.name == "hr" and not request.user.is_superuser:
        messages.error(request, "You do not have permission to register employees.")
        return redirect("employee_list")

    if request.method == "POST":
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            role = Role.objects.get(name=form.cleaned_data["role"])
            employee = Employee.objects.create(user=user, name=form.cleaned_data["name"], role=role)
            messages.success(request, f"Employee {employee.name} registered successfully.")
            return redirect("employee_list")
    else:
        form = EmployeeRegistrationForm()

    return render(request, "manage_panel/register_employee.html", {"form": form})

@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.user.is_superuser or request.user.employee.role.name == "hr":
        employee.user.delete()  # Deletes user and employee entry
        messages.success(request, "Employee deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete employees.")

    return redirect("employee_list")

@login_required
def update_employee_role(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if not request.user.is_superuser and request.user.employee.role.name != "hr":
        messages.error(request, "You do not have permission to change roles.")
        return redirect("employee_list")

    if request.method == "POST":
        new_role = request.POST.get("role")
        role = Role.objects.get(name=new_role)
        employee.role = role
        employee.save()
        messages.success(request, f"{employee.name} is now {new_role}.")
        return redirect("employee_list")

    roles = Role.objects.all()
    return render(request, "manage_panel/update_role.html", {"employee": employee, "roles": roles})


@login_required
def manage_panel(request):
    employees = Employee.objects.all()
    return render(request, "manage_panel.html", {"employees": employees})