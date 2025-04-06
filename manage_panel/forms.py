from django import forms
from employees.models import Employee, Role
from datetime import date

class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        required=False  # Пароль необязателен
    )

    class Meta:
        model = Employee
        fields = [
            'email', 'password', 'name', 'role', 'age', 'salary', 'department',
            'hiring_date', 'bonuses', 'work_experience'
        ]
        labels = {
            'email': 'Email',
            'name': 'Имя',
            'role': 'Роль',
            'age': 'Возраст',
            'salary': 'Зарплата',
            'department': 'Отдел',
            'hiring_date': 'Дата найма',
            'bonuses': 'Бонусы',
            'work_experience': 'Опыт работы (годы)',
        }
        widgets = {
            'hiring_date': forms.DateInput(attrs={'type': 'date'}),
            'role': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.all()

        # Для нового сотрудника устанавливаем текущую дату
        if not self.instance.pk:
            self.fields['role'].initial = Role.objects.get(name='employee')
            self.fields['hiring_date'].initial = date.today()
        # При редактировании убираем поле hiring_date
        else:
            if 'hiring_date' in self.fields:
                del self.fields['hiring_date']  # Удаляем поле из формы при редактировании

    def save(self, commit=True):
        employee = super().save(commit=False)
        # Устанавливаем пароль, если он указан
        if self.cleaned_data.get('password'):
            employee.set_password(self.cleaned_data['password'])
        elif not employee.pk and not employee.has_usable_password():
            employee.set_unusable_password()  # Только для нового сотрудника
        if commit:
            employee.save()
        return employee