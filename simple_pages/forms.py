from django import forms
from employees.models import Employee

class CVUploadForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["cv_file"]
