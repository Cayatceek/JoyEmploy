from django.db import models
from employees.models import Employee

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название задачи")
    status = models.CharField(
        max_length=50,
        choices=[('pending', 'В ожидании'), ('completed', 'Завершена')],
        default='pending',
        verbose_name="Статус"
    )
    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="taskboard_tasks",  # Изменён related_name, чтобы не конфликтовать с employees.Task
        verbose_name="Назначенный сотрудник"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Новые задачи сверху по умолчанию