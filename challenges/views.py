from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from .models import SkillChallenge, ChallengeParticipation, UserAchievement, UserPoints
from .forms import ChallengeForm, SubmissionForm

@login_required
def challenge_list(request):
    active_challenges = SkillChallenge.objects.filter(
        end_date__gte=timezone.now()
    ).annotate(
        participants_count=Count('challengeparticipation')
    ).order_by('start_date')
    
    user_participations = ChallengeParticipation.objects.filter(
        user=request.user
    ).values_list('challenge_id', flat=True)
    
    context = {
        'active_challenges': active_challenges,
        'user_participations': user_participations,
    }
    return render(request, 'challenges/challenge_list.html', context)

@login_required
def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.creator = request.user
            challenge.save()
            messages.success(request, 'Challenge created successfully!')
            return redirect('challenge_detail', pk=challenge.pk)
    else:
        form = ChallengeForm()
    
    return render(request, 'challenges/challenge_form.html', {'form': form})

@login_required
def challenge_detail(request, pk):
    challenge = get_object_or_404(SkillChallenge, pk=pk)
    user_participation = ChallengeParticipation.objects.filter(
        user=request.user,
        challenge=challenge
    ).first()
    
    if request.method == 'POST' and not user_participation:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            participation = form.save(commit=False)
            participation.user = request.user
            participation.challenge = challenge
            participation.save()
            messages.success(request, 'Submission uploaded successfully!')
            return redirect('challenge_detail', pk=pk)
    else:
        form = SubmissionForm()
    
    participants = ChallengeParticipation.objects.filter(challenge=challenge)
    
    context = {
        'challenge': challenge,
        'user_participation': user_participation,
        'form': form,
        'participants': participants,
    }
    return render(request, 'challenges/challenge_detail.html', context)

@login_required
def user_achievements(request):
    achievements = UserAchievement.objects.filter(user=request.user).order_by('-earned_date')
    try:
        points = UserPoints.objects.get(user=request.user)
    except UserPoints.DoesNotExist:
        points = UserPoints.objects.create(user=request.user)
    
    context = {
        'achievements': achievements,
        'points': points,
    }
    return render(request, 'challenges/user_achievements.html', context)

@login_required
def edit_challenge(request, pk):
    challenge = get_object_or_404(SkillChallenge, pk=pk)
    if challenge.creator != request.user:
        messages.error(request, 'You do not have permission to edit this challenge.')
        return redirect('challenge_detail', pk=pk)
    
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, 'Challenge updated successfully!')
            return redirect('challenge_detail', pk=pk)
    else:
        form = ChallengeForm(instance=challenge)
    
    return render(request, 'challenges/challenge_form.html', {'form': form, 'challenge': challenge})
