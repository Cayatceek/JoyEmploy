from django.urls import path
from .views import taskboard_view

urlpatterns = [
    path('', taskboard_view, name='taskboard_view'),
]
