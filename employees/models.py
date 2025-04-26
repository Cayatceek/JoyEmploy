from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date

class Role(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('hr', 'HR'),
        ('superadmin', 'Суперадмин'),
    ]
    name = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True,
        default='employee',  # Добавлено значение по умолчанию
        verbose_name="Название роли"
    )

    def __str__(self):
        return self.name

class EmployeeManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """Создание обычного пользователя"""
        if not email:
            raise ValueError("Поле Email обязательно для заполнения")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.objects.get_or_create(name='superadmin')[0])

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")  # Без default, так как обязательное поле
    name = models.CharField(max_length=100, verbose_name="Имя")  # Без default, так как в REQUIRED_FIELDS
    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,  # Оставляем возможность null, но можно указать Role.objects.get(name='employee')
        verbose_name="Роль"
    )
    tasks_completed = models.IntegerField(default=0, verbose_name="Завершённые задачи")
    work_hours = models.FloatField(default=0.0, verbose_name="Рабочие часы")
    age = models.IntegerField(default=18, verbose_name="Возраст")
    hiring_date = models.DateField(default=date.today, verbose_name="Дата найма")  # Уже есть default
    work_experience = models.FloatField(default=0.0, verbose_name="Опыт работы (годы)")
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00, verbose_name="Зарплата")
    department = models.CharField(max_length=100, default="General", verbose_name="Отдел")  # Уже есть default
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Бонусы")
    cv_file = models.FileField(upload_to="cvs/", null=True, blank=True, verbose_name="Файл резюме")
    cv_text = models.TextField(null=True, blank=True, default="", verbose_name="Текст резюме")  # Добавлен default
    cv_analysis = models.TextField(null=True, blank=True, default="", verbose_name="Анализ резюме")  # Добавлен default

    # Поля, необходимые для кастомной модели пользователя
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник админки")

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'  # Поле для входа (вместо username)
    REQUIRED_FIELDS = ['name']  # Обязательные поля при создании суперпользователя

    @property
    def days_worked(self):
        return max((date.today() - self.hiring_date).days, 1)

    @property
    def efficiency_score(self):
        return round(self.tasks_completed / self.days_worked, 2)

    def __str__(self):
        return f"{self.name} ({self.role.name if self.role else 'Без роли'})"