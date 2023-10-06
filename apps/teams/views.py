from django.shortcuts import render
from .models import Team, TeamMember
from django.views.generic import CreateView, UpdateView, ListView, FormView, TemplateView
from django.urls import reverse_lazy
from django import forms
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

class TeamCreateView(CreateView):
    model = Team
    fields = ['team_name', "zp_id"]
    template_name = 'team_form.html'
    success_url = reverse_lazy('teams:team_list')

class TeamUpdateView(UpdateView):
    model = Team
    fields = ['team_name', 'zp_id']
    template_name = 'team_form.html'
    success_url = reverse_lazy('teams:team_list')

class TeamListView(ListView):
    model = Team
    template_name = 'team_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Team.objects.filter(Q(team_name__icontains=query))
        return Team.objects.all()


class JoinTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())

class JoinTeamView(LoginRequiredMixin, FormView):
    form_class = JoinTeamForm
    template_name = 'team_join.html'
    success_url = reverse_lazy('teams:team_list')

    @transaction.atomic
    def form_valid(self, form):
        team = form.cleaned_data['team']
        
        # Check if the user is already a member of the team
        if TeamMember.objects.filter(user=self.request.user, team=team).exists():
            messages.error(self.request, 'You are already a member of this team.')
            return super().form_invalid(form)
        
        try:
            team_member = TeamMember.objects.create(user=self.request.user)
            team_member.team.add(team)  
            messages.success(self.request, 'Successfully joined the team!')
        except IntegrityError:
            messages.error(self.request, 'There was an error joining the team. Please try again.')
            return super().form_invalid(form)

        return super().form_valid(form)

    
class TeamAdminView(ListView):
    model = TeamMember
    template_name = 'team_members_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.get(id=self.kwargs['team_id'])
        return context
    
    def get_queryset(self):
        team = self.kwargs['team_id']
        return TeamMember.objects.filter(team=team)

class JoinTeamIDView(LoginRequiredMixin, TemplateView):
    template_name = "team_join.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        team_id = self.kwargs.get('team_id')
        
        # Initialize the form with the passed team_id.
        context['form'] = JoinTeamForm(initial={'team': team_id})
        
        return context