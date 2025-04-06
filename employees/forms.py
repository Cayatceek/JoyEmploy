from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee, Role

class EmployeeAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)  

    class Meta:
        model = Employee
        fields = ['username', 'password']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Email" 
