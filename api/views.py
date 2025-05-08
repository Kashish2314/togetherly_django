from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import User, UserProfile
from messaging.models import Message, Conversation
from connections.models import Connection
from notifications.models import Notification
from challenges.models import SkillChallenge, ChallengeParticipation
from .serializers import (
    UserSerializer, MessageSerializer, ConversationSerializer,
    ConnectionSerializer, NotificationSerializer, ChallengeSerializer,
    ChallengeParticipantSerializer
)
from django.db.models import Q

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all users
        for the currently authenticated user.
        """
        return User.objects.all().order_by('-date_joined')

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                conversation=conversation,
                sender=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Connection.objects.filter(
            sender=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        connection = self.get_object()
        if connection.receiver == request.user:
            connection.status = 'accepted'
            connection.save()
            return Response({'status': 'connection accepted'})
        return Response(status=status.HTTP_403_FORBIDDEN)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SkillChallenge.objects.filter(
            Q(creator=self.request.user) |  # Challenges created by user
            Q(challengeparticipation__user=self.request.user)  # Challenges user is participating in
        ).distinct().order_by('-created_at')

    def perform_create(self, serializer):
        challenge = serializer.save(creator=self.request.user)
        # The signal will handle incrementing challenges_created

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        challenge = self.get_object()
        if challenge.get_participants_count() >= challenge.max_participants:
            return Response(
                {'error': 'Challenge is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        participant, created = ChallengeParticipation.objects.get_or_create(
            challenge=challenge,
            user=request.user,
            defaults={'status': 'pending'}
        )
        if not created:
            return Response(
                {'error': 'Already participating'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'status': 'joined challenge'})

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        challenge = self.get_object()
        if challenge.creator != request.user:
            return Response(
                {'error': 'Only challenge creator can view participants'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        participants = ChallengeParticipation.objects.filter(challenge=challenge)
        serializer = ChallengeParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        challenge = self.get_object()
        try:
            participation = ChallengeParticipation.objects.get(
                challenge=challenge,
                user=request.user
            )
            if participation.status != 'accepted':
                return Response(
                    {'error': 'Challenge must be accepted before completion'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            participation.status = 'completed'
            participation.save()
            # The signal will handle incrementing challenges_completed
            
            return Response({'status': 'challenge completed'})
        except ChallengeParticipation.DoesNotExist:
            return Response(
                {'error': 'Not participating in this challenge'},
                status=status.HTTP_404_NOT_FOUND
            )

class ChallengeParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChallengeParticipation.objects.filter(
            user=self.request.user
        ).order_by('-submitted_at')
