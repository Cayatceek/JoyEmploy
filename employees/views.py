from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
