from django import forms
from .models import Team

class JoinTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', "zp_id"]