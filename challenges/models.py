from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class SkillChallenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('business', 'Business Strategy'),
        ('writing', 'Content Writing'),
        ('data', 'Data Analysis')
    ]
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    max_participants = models.IntegerField(default=50)
    prize_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='challenge_images/', null=True, blank=True)
    
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    def get_participants_count(self):
        return self.challengeparticipation_set.count()

class ChallengeParticipation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(SkillChallenge, on_delete=models.CASCADE)
    submission = models.FileField(upload_to='challenge_submissions/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    evaluation_score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

class UserAchievement(models.Model):
    BADGE_TYPES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(SkillChallenge, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    earned_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

class UserPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
