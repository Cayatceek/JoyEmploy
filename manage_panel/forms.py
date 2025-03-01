from django import forms
from employees.models import Role

class EmployeeRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=[(role.name, role.name) for role in Role.objects.all()])
