from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    challenges_created = models.IntegerField(default=0)
    challenges_completed = models.IntegerField(default=0)

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return "https://static.vecteezy.com/system/resources/previews/005/544/718/non_2x/profile-icon-design-free-vector.jpg"

    def increment_challenges_created(self):
        self.challenges_created += 1
        self.save()

    def increment_challenges_completed(self):
        self.challenges_completed += 1
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
