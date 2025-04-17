from django import forms
from .models import SkillChallenge, ChallengeParticipation

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = SkillChallenge
        fields = ['title', 'description', 'difficulty', 'category', 'start_date', 
                 'end_date', 'max_participants', 'prize_description', 'image']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = ChallengeParticipation
        fields = ['submission'] 