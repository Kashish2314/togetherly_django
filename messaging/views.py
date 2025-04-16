# messaging/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model  # Add this import

# Get the User model
User = get_user_model()

# Import your other models
from .models import Conversation, Message
from users.models import UserProfile  # Adjust if your UserProfile is elsewhere

@login_required
def messaging_home(request):
    # Get all users except the current user and superusers
    all_users = User.objects.exclude(
        Q(id=request.user.id) |  # Exclude current user
        Q(is_superuser=True)     # Exclude superusers
    ).select_related('userprofile').order_by('username')
    
    # Get active conversation if any
    active_conversation = None
    messages = []
    other_user = None
    
    return render(request, 'messaging/messaging.html', {
        'all_users': all_users,
        'active_conversation': active_conversation,
        'messages': messages,
        'other_user': other_user
    })

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id, 
        participants=request.user  
    )
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            # Mark other messages as read
            conversation.messages.exclude(sender=request.user).update(read=True)
            return redirect('conversation_detail', conversation_id=conversation.id)
    
    # Get all conversations for the sidebar
    conversations = request.user.conversations.all()
    messages = conversation.messages.all()
    
    return render(request, 'messaging/messaging.html', {
        'conversations': conversations,
        'active_conversation': conversation,
        'messages': messages,
        'other_user': conversation.get_other_participant(request.user)
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

@login_required
def get_conversations(request):
    conversations = request.user.conversations.all().order_by('-updated_at')
    data = [{
        'id': conv.id,
        'other_user': conv.get_other_participant(request.user).get_full_name() or conv.get_other_participant(request.user).username,
        'last_message': conv.get_last_message().content if conv.get_last_message() else '',
        'timestamp': conv.updated_at.strftime("%b %d, %Y %I:%M %p"),
        'unread': conv.messages.filter(read=False).exclude(sender=request.user).count()
    } for conv in conversations]
    
    return JsonResponse(data, safe=False)

@login_required
def check_new_messages(request, conversation_id):
    last_message_id = request.GET.get('last_id', 0)
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    new_messages = Message.objects.filter(
        conversation=conversation,
        id__gt=last_message_id
    ).exclude(sender=request.user).order_by('timestamp')
    
    return JsonResponse({
        'new_messages': [
            {
                'id': msg.id,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'sender': msg.sender.username
            } for msg in new_messages
        ]
    })