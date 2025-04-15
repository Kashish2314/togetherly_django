from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.base, name='landing'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('user_profile/', views.profile, name='profile'),
]