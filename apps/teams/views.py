from django.shortcuts import render
from .models import Team, TeamMember
from django.views.generic import CreateView, UpdateView, ListView, FormView, TemplateView, DetailView
from django.urls import reverse_lazy
from django import forms
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Team
from .forms import TeamForm
from django.http import JsonResponse
from apps.zp import fetch
from veloteams.users.models import User 
class TeamListViewCreate(View):
    template_name = 'team_list.html'
    form_class = TeamForm
    success_url = reverse_lazy('teams:team_list')

    def get(self, request):
        teams = Team.objects.all()
        query = self.request.GET.get('q')
        if query:
            teams = teams.filter(Q(team_name__icontains=query))
        form = self.form_class()
        return render(request, self.template_name, {'teams': teams, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        if self._is_ajax(request):
            return self._handle_ajax_request(form)
        
        return self._handle_standard_request(form)

    def _is_ajax(self, request):
        """Helper function to determine if request is AJAX."""
        return 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest'

    def _handle_ajax_request(self, form):
        """Handle AJAX form submission."""
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        
        return JsonResponse({'errors': form.errors})

    def _handle_standard_request(self, form):
        """Handle standard form submission."""
        if form.is_valid():
            return redirect(self.success_url)
        
        teams = Team.objects.all()
        return render(request, self.template_name, {'teams': teams, 'form': form, 'errors': form.errors})

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

class TeamProfileView(DetailView):
    model = Team
    template_name = 'team_profile.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        zp = fetch.ZPSession()
        team_zp_id = self.object.zp_id
        team_riders_response = zp.get_api(team_zp_id, 'team_riders')
        team_riders_data = team_riders_response.get('team_riders', {}).get('data', [])
        
        team_members = []
        for rider_data in team_riders_data:
            # Assuming the rider's name is unique and is used as the username for the User model
            username = rider_data['name']
            
            # Get or create the user object based on the name (or any other unique criteria)
            user, _ = User.objects.get_or_create(name=username, defaults={'email': rider_data['email']})

            # Here, I assume the owner status is determined by the 'status' field from the API response
            is_owner = True if rider_data['status'] == 'Owner' else False

            # Create or update the TeamMember object
            team_member, _ = TeamMember.objects.update_or_create(
                user=user,
                defaults={
                    'is_owner': is_owner,
                    # ... any other fields  want to set or update
                }
            )
            
            # Add the current team to the team_member's many-to-many relation
            team_member.team.add(self.object)

            team_members.append(team_member)

        # Add the team members to the context
        context['team_members'] = team_members

        # If  have similar logic for team results, do the same for them.

        return context