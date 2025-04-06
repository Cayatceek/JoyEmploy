from django.urls import path
from .views import  employee_detail, UploadCV

urlpatterns = [
    path('employee/<int:employee_id>/', employee_detail, name='employee_detail'),
    path('employee/<int:employee_id>/upload-cv/', UploadCV.as_view(), name='upload_cv'),

]
