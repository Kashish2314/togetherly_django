from django.urls import path
from . import views

urlpatterns = [
    path('', views.connections, name='connections'),
]