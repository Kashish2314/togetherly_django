from rest_framework import serializers
from users.models import User
from messaging.models import Message, Conversation
from connections.models import Connection
from notifications.models import Notification
from challenges.models import SkillChallenge, ChallengeParticipation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['email']  # Make email read-only for security 

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp', 'read']
        read_only_fields = ['sender', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = MessageSerializer(read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'last_message']

class ConnectionSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = Connection
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']
        read_only_fields = ['sender', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'notification_type', 'content', 'is_read', 'created_at']
        read_only_fields = ['recipient', 'created_at']

class ChallengeParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ChallengeParticipation
        fields = ['id', 'challenge', 'user', 'status', 'submitted_at', 'evaluation_score', 'feedback']
        read_only_fields = ['submitted_at']

class ChallengeSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    participants = ChallengeParticipantSerializer(many=True, read_only=True)
    
    class Meta:
        model = SkillChallenge
        fields = ['id', 'title', 'description', 'creator', 'start_date', 'end_date', 
                 'difficulty', 'category', 'max_participants', 'prize_description',
                 'participants', 'created_at', 'image']
        read_only_fields = ['creator', 'created_at'] 