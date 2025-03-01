from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('hr', 'HR'),
        ('superadmin', 'Super Admin'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    tasks_completed = models.IntegerField(default=0)
    work_hours = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    assigned_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title
