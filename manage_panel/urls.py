from django.urls import path
from .views import register_employee, delete_employee, manage_panel, employee_list, edit_employee


urlpatterns = [
    path("register/", register_employee, name="register_employee"),
    path("delete/<int:employee_id>/", delete_employee, name="delete_employee"),
    path('employees/', employee_list, name='employee_list'),
    path("manage/", manage_panel, name="manage_panel"),
    path('employees/edit/<int:employee_id>/', edit_employee, name='update_employee'),
]
