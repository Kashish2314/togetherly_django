from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # username, password, email, first_name, last_name are already included
    email = models.EmailField(unique=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
