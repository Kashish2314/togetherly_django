from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from users.models import User, UserProfile
from .models import Connection
from messaging.models import Conversation
from django.contrib import messages
from django.contrib.auth import get_user_model
from notifications.models import Notification
from django.db import models

User = get_user_model()

# Create your views here.
@login_required
def connections(request):
    # Get all users except current user and those already connected
    connected_users = Connection.objects.filter(
        (Q(sender=request.user) | Q(receiver=request.user)),
        status='accepted'
    ).values_list('sender', 'receiver')
    
    # Get pending requests sent by current user
    pending_sent_ids = Connection.objects.filter(
        sender=request.user, 
        status='pending'
    ).values_list('receiver_id', flat=True)

    # Get pending requests received by current user
    pending_received = Connection.objects.filter(
        receiver=request.user, 
        status='pending'
    ).select_related('sender')
    
    # Get users to suggest (not connected and no pending requests)
    suggested_users = User.objects.exclude(
        Q(id__in=pending_sent_ids) |
        Q(id=request.user.id) |
        Q(is_superuser=True)
    ).select_related('userprofile')

    context = {
        'user': request.user,
        'suggested_users': suggested_users,
        'pending_sent_ids': list(pending_sent_ids),
        'pending_received': pending_received,
    }
    
    return render(request, 'connections/connections.html', context)

@login_required
def send_connection_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    
    if request.user == receiver:
        messages.error(request, "You cannot connect with yourself.")
        return redirect('profile', username=receiver.username)
        
    connection, created = Connection.objects.get_or_create(
        sender=request.user,
        receiver=receiver,
        defaults={'status': 'pending'}
    )
    
    if created:
        messages.success(request, f"Connection request sent to {receiver.username}")
    else:
        messages.info(request, f"Connection request already exists with {receiver.username}")
    
    return redirect('profile', username=receiver.username)

@login_required
def handle_connection_request(request, connection_id):
    connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
    action = request.POST.get('action')
    
    if action == 'accept':
        connection.status = 'accepted'
        connection.save()
        messages.success(request, f"You are now connected with {connection.sender.username}")
    elif action == 'reject':
        connection.status = 'rejected'
        connection.save()
        messages.info(request, f"Connection request from {connection.sender.username} rejected")
    
    # Mark notification as read
    Notification.objects.filter(connection=connection, recipient=request.user).update(is_read=True)
    
    return redirect('notifications')

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Find existing conversation or create a new one
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
    
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def connection_list(request):
    connections = Connection.objects.filter(
        status='accepted'
    ).filter(
        models.Q(sender=request.user) | models.Q(receiver=request.user)
    )
    return render(request, 'connections/connection_list.html', {'connections': connections})

@login_required
def get_connection_count(request, user_id):
    user = get_object_or_404(User, id=user_id)
    count = Connection.objects.filter(
        models.Q(sender=user) | models.Q(receiver=user),
        status='accepted'
    ).count()
    return JsonResponse({'count': count})