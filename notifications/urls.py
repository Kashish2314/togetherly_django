from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notifications'),
    path('count/', views.get_notification_count, name='get_notification_count'),
]