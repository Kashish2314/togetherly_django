from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenge_list, name='challenge_list'),
    path('create/', views.create_challenge, name='create_challenge'),
    path('<int:pk>/', views.challenge_detail, name='challenge_detail'),
    path('<int:pk>/edit/', views.edit_challenge, name='challenge_form'),
    path('achievements/', views.user_achievements, name='user_achievements'),
] 