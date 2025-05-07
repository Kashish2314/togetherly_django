from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'connections', views.ConnectionViewSet, basename='connection')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'challenges', views.ChallengeViewSet, basename='challenge')
router.register(r'challenge-participants', views.ChallengeParticipantViewSet, basename='challenge-participant')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),  # Adds login/logout views
] 