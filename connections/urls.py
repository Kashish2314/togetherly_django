from django.urls import path
from . import views

urlpatterns = [
    path('', views.connections, name='connections'),
    path('send-request/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
    path('handle-request/<int:connection_id>/', views.handle_connection_request, name='handle_connection_request'),
    path('list/', views.connection_list, name='connection_list'),
    path('count/<int:user_id>/', views.get_connection_count, name='get_connection_count'),
    path('start_conversation/<int:user_id>/', views.start_conversation, name='start_conversation'),
]