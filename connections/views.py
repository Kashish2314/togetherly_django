from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from users.models import User, UserProfile
from .models import Connection
from messaging.models import Conversation

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
    if request.method == 'POST':
        try:
            receiver = User.objects.get(id=user_id)
            
            # Check if connection already exists
            existing_connection = Connection.objects.filter(
                (Q(sender=request.user, receiver=receiver) |
                Q(sender=receiver, receiver=request.user))
            ).first()
            
            if existing_connection:
                return JsonResponse({
                    'success': False,
                    'message': 'Connection request already exists'
                })
            
            # Create new connection request
            Connection.objects.create(sender=request.user, receiver=receiver)
            
            return JsonResponse({
                'success': True,
                'message': 'Connection request sent successfully'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User not found'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
def handle_connection_request(request, connection_id):
    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            connection = Connection.objects.get(id=connection_id, receiver=request.user)
            
            if action == 'accept':
                connection.status = 'accepted'
                connection.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Connection request accepted'
                })
            elif action == 'reject':
                connection.status = 'rejected'
                connection.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Connection request rejected'
                })
            
        except Connection.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Connection request not found'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

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