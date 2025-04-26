from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from employees.models import Employee
from django.utils import timezone  # Добавляем для работы с датой

@login_required
def taskboard_view(request):
    current_employee = request.user
    # Админы — это superadmin или hr
    is_admin = current_employee.is_superuser or (current_employee.role and current_employee.role.name in ['hr', 'superadmin'])

    if request.method == 'POST':
        if 'delete' in request.POST and is_admin:
            task_id = request.POST.get('delete')
            Task.objects.filter(id=task_id).delete()
            return redirect('taskboard_view')

        elif 'complete' in request.POST:
            task_id = request.POST.get('complete')
            task = Task.objects.get(id=task_id)
            # Только владелец задачи может её завершить
            if task.assigned_employee == current_employee:
                task.status = 'completed'
                task.completed_at = timezone.now()  # Устанавливаем дату завершения
                task.save()
                # Увеличиваем счётчик завершённых задач
                task.assigned_employee.tasks_completed += 1
                task.assigned_employee.save()
            return redirect('taskboard_view')

        elif 'title' in request.POST and is_admin:
            title = request.POST.get('title')
            employee_id = request.POST.get('employee')
            if title and employee_id:
                try:
                    employee = Employee.objects.get(id=employee_id)
                    Task.objects.create(
                        title=title,
                        assigned_employee=employee
                    )
                except Employee.DoesNotExist:
                    pass
                return redirect('taskboard_view')

    if is_admin:
        tasks = Task.objects.select_related('assigned_employee').all()
    else:
        tasks = Task.objects.select_related('assigned_employee').filter(assigned_employee=current_employee)

    pending_tasks = tasks.filter(status='pending')
    completed_tasks = tasks.filter(status='completed')
    employees = Employee.objects.all() if is_admin else None

    return render(request, 'taskboard/taskboard.html', {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'employees': employees,
        'is_admin': is_admin,
    })