from django.urls import path
from . import views

urlpatterns = [
    path('', views.messaging_home, name='messaging'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('api/conversations/', views.get_conversations, name='get_conversations'),
    path('conversation/<int:conversation_id>/check_new/', views.check_new_messages, name='check_new_messages'),
]