from django.urls import path
from . import views

urlpatterns = [
    path('', views.connections, name='connections'),
    path('send_request/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
    path('handle_request/<int:connection_id>/', views.handle_connection_request, name='handle_connection_request'),
    path('start_conversation/<int:user_id>/', views.start_conversation, name='start_conversation'),
]