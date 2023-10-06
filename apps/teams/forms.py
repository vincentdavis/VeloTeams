from django import forms
from .models import Team

class JoinTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())
