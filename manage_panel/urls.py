from django.urls import path
from .views import register_employee, delete_employee, update_employee_role, manage_panel


urlpatterns = [
    path("register/", register_employee, name="register_employee"),
    path("delete/<int:employee_id>/", delete_employee, name="delete_user"),
    path("update_role/<int:employee_id>/", update_employee_role, name="update_role"),
    path("manage/", manage_panel, name="manage_panel"),
]
