from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from .models import User, UserProfile, Post
from connections.models import Connection
from django.db.models import Q

def base(request):
    return render(request, 'users/base.html')

def load(request):
    return render(request, 'users/load.html')

def home(request):
    # If user is superuser but came from admin site, don't use that session
    if request.user.is_superuser and request.META.get('HTTP_REFERER', '').find('/admin/') != -1:
        # Clear the session for this view only
        auth_logout(request)
    
    # Rest of your view logic
    return render(request, 'users/home.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email does not exist. Please register first.')
            return render(request, 'users/login.html')
        user = authenticate(request, username=user.username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('load')
        else:
            messages.error(request, 'Invalid password!')
    return render(request, 'users/login.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('signup')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    return render(request, 'users/signup.html')


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'username': request.user.username,
            'email': request.user.email,
        }
    )
    
    # Get post count for the user
    post_count = Post.objects.filter(user=request.user).count()
    
    # Get connection count
    connection_count = Connection.objects.filter(
        Q(sender=request.user, status='accepted') | 
        Q(receiver=request.user, status='accepted')
    ).count()
    
    skills = [s.strip() for s in user_profile.skills.split(',')] if user_profile.skills else []
    
    return render(request, 'users/userprofile.html', {
        'user': request.user,
        'user_profile': user_profile,
        'skills': skills,
        'post_count': post_count,
        'connection_count': connection_count,
        'challenges_created': user_profile.challenges_created,
        'challenges_completed': user_profile.challenges_completed,
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        
        # Update other fields
        user_profile.name = request.POST.get('name')
        user_profile.username = request.POST.get('username')
        user_profile.email = request.POST.get('email')
        user_profile.bio = request.POST.get('bio')
        user_profile.skills = request.POST.get('skills')
        user_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    messages.error(request, 'Invalid request.')
    return redirect('profile')


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        auth_logout(request)
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('landing')
    return HttpResponseForbidden()

@login_required
def create_post(request):
    if request.method == 'POST':
        try:
            content = request.POST.get('content')
            if not content:
                return JsonResponse({
                    'success': False,
                    'message': 'Post content cannot be empty.'
                }, status=400)
            
            post = Post.objects.create(user=request.user, content=content)
            
            return JsonResponse({
                'success': True,
                'message': 'Post created successfully!',
                'post': {
                    'id': post.id,
                    'content': post.content,
                    'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'username': request.user.username,
                    'user_id': request.user.id,
                    'profile_picture_url': request.user.userprofile.get_profile_picture_url()
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
            
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)

@login_required
def get_posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    post_list = []
    for post in posts:
        post_list.append({
            'id': post.id,
            'content': post.content,
            'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'username': post.user.username,
            'user_id': post.user.id,
            'profile_picture_url': post.user.userprofile.get_profile_picture_url()
        })
    return JsonResponse({'success': True, 'posts': post_list})

@login_required
def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            return JsonResponse({'success': False, 'message': 'You can only delete your own posts.'}, status=403)
        try:
            post.delete()
            # Get updated post count
            post_count = Post.objects.filter(user=request.user).count()
            return JsonResponse({
                'success': True, 
                'message': 'Post deleted successfully!',
                'post_count': post_count
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def edit_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            return JsonResponse({'success': False, 'message': 'You can only edit your own posts.'}, status=403)
        try:
            content = request.POST.get('content', '').strip()
            if not content:
                return JsonResponse({
                    'success': False,
                    'message': 'Post content cannot be empty.'
                }, status=400)
            
            post.content = content
            post.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Post updated successfully!',
                'post': {
                    'id': post.id,
                    'content': post.content,
                    'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'username': post.user.username,
                    'user_id': post.user.id
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

