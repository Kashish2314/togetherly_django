from django.contrib import admin
from .models import SkillChallenge, ChallengeParticipation, UserAchievement, UserPoints

@admin.register(SkillChallenge)
class SkillChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'difficulty', 'category', 'start_date', 'end_date', 'max_participants')
    list_filter = ('difficulty', 'category', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'creator__username')
    date_hierarchy = 'start_date'

@admin.register(ChallengeParticipation)
class ChallengeParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'status', 'submitted_at', 'evaluation_score')
    list_filter = ('status', 'submitted_at')
    search_fields = ('user__username', 'challenge__title', 'feedback')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'badge_type', 'earned_date')
    list_filter = ('badge_type', 'earned_date')
    search_fields = ('user__username', 'challenge__title', 'description')

@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_points', 'level')
    search_fields = ('user__username',)
    ordering = ('-total_points',)
