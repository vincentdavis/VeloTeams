from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render
import datetime
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from django.views.generic.edit import FormView

from apps.zp.models import TeamRiders, Profile

from .forms import TeamForm
from .models import Team, TeamMember


class TeamListViewCreate(View):
    template_name = "team_list.html"
    form_class = TeamForm
    success_url = reverse_lazy("teams:team_list")

    def get(self, request):
        teams = Team.objects.all()
        query = self.request.GET.get("q")
        if query:
            teams = teams.filter(Q(team_name__icontains=query))
        form = self.form_class()
        return render(request, self.template_name, {"teams": teams, "form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if self._is_ajax(request):
            return self._handle_ajax_request(form)

        return self._handle_standard_request(form)

    def _is_ajax(self, request):
        """Helper function to determine if request is AJAX."""
        return (
            "HTTP_X_REQUESTED_WITH" in request.META
            and request.META["HTTP_X_REQUESTED_WITH"] == "XMLHttpRequest"
        )

    def _handle_ajax_request(self, form):
        """Handle AJAX form submission."""
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"})

        return JsonResponse({"errors": form.errors})

    def _handle_standard_request(self, form):
        """Handle standard form submission."""
        if form.is_valid():
            return redirect(self.success_url)

        teams = Team.objects.all()
        return render(
            request,
            self.template_name,
            {"teams": teams, "form": form, "errors": form.errors},
        )


class TeamCreateView(CreateView):
    model = Team
    fields = ["team_name", "zp_id"]
    template_name = "team_form.html"
    success_url = reverse_lazy("teams:team_list")


class TeamUpdateView(UpdateView):
    model = Team
    fields = ["team_name", "zp_id"]
    template_name = "team_form.html"
    success_url = reverse_lazy("teams:team_list")


class TeamListView(ListView):
    model = Team
    template_name = "team_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Team.objects.filter(Q(team_name__icontains=query))
        return Team.objects.all()


class JoinTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())


class JoinTeamView(LoginRequiredMixin, FormView):
    form_class = JoinTeamForm
    template_name = "team_join.html"
    success_url = reverse_lazy("teams:team_list")

    @transaction.atomic
    def form_valid(self, form):
        team = form.cleaned_data["team"]

        # Check if the user is already a member of the team
        if TeamMember.objects.filter(user=self.request.user, team=team).exists():
            messages.error(self.request, "You are already a member of this team.")
            return super().form_invalid(form)

        try:
            team_member = TeamMember.objects.create(user=self.request.user)
            team_member.team.add(team)
            messages.success(self.request, "Successfully joined the team!")
        except IntegrityError:
            messages.error(
                self.request, "There was an error joining the team. Please try again."
            )
            return super().form_invalid(form)

        return super().form_valid(form)


class TeamAdminView(ListView):
    model = TeamMember
    template_name = "team_members_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = Team.objects.get(id=self.kwargs["team_id"])
        return context

    def get_queryset(self):
        team = self.kwargs["team_id"]
        return TeamMember.objects.filter(team=team)


class JoinTeamIDView(LoginRequiredMixin, TemplateView):
    template_name = "team_join.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        team_id = self.kwargs.get("team_id")

        # Initialize the form with the passed team_id.
        context["form"] = JoinTeamForm(initial={"team": team_id})

        return context


class TeamProfileView(DetailView):
    model = Team
    template_name = "team_profile.html"
    context_object_name = "team"

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        Override this method to use 'custom_field' for lookup instead of 'pk'.
        """
        if queryset is None:
            queryset = self.get_queryset()

        # Get the 'custom_field' value from the URL.
        custom_field = self.kwargs.get('zp_id')

        # Perform the lookup filtering.
        if custom_field is not None:
            queryset = queryset.filter(zp_id=custom_field)

        # Ensure  get one object, and raise a 404 if not found.
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            team_riders, created = TeamRiders.objects.get_or_create(zp_id=self.object.zp_id, )
            context["team_members"] = team_riders.team_riders
        except Exception as e:
            pass

        return context


class TeamAuditReportView(View):
    def get_report_data(self, team_id, search=None, sort=None, page=1):
        """
        Fetches report data based on team_id, with optional search, sort, and pagination.

        :param team_id: ID of the team.
        :param search: Optional search term for filtering by team name.
        :param sort: Optional sort order.
        :param page: Page number for pagination.
        :return: A page of sorted and/or filtered report data.
        """
        try:
            team_riders = TeamRiders.objects.filter(zp_id=team_id).latest('modified_at')
        except TeamRiders.DoesNotExist:
            # Handle the case where no team riders are found
            return render(request, 'error.html', {'message': 'Team not found'})

        # Extract profile zwids
        profile_ids = [rider.get('zwid') for rider in team_riders.team_riders if rider.get('zwid')]

        # Fetch corresponding profiles
        queryset = Profile.objects.filter(zp_id__in=profile_ids)

        # Annotate to extract the 'name' from the first element of the JSON array
        queryset = queryset.annotate(
            profile__name=F('profile__0__name'),
            profile__tname=F('profile__0__tname'),
        )

        if search:
            queryset = queryset.filter(profile__icontains=search)
        if sort:
            queryset = queryset.order_by(sort)

        paginator = Paginator(queryset, 10)  # 10 profiles per page
        return paginator.get_page(page), None

    def get(self, request, team_id):
        search = request.GET.get('search', '')
        sort = request.GET.get('sort', '')
        page = request.GET.get('page', 1)
        report_data, error = self.get_report_data(team_id, search=search, sort=sort, page=page)
        if error:
            return render(request, 'error.html', {'message': error})

        context = {
            'report_data': report_data,
            'search': search,
            'sort': sort
        }
        return render(request, 'team_audit_report.html', context)

    def post(self, request, team_id):
        action = request.POST.get('action', '')

        if action == 'export':
            report_data, error = self.get_report_data(team_id)
            if error:
                return render(request, 'error.html', {'message': error})

            # Convert report data to a Pandas DataFrame
            df = pd.DataFrame(report_data)

            # Create a CSV response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="team_audit_report_{team_id}.csv"'

            # Use Pandas to write the DataFrame to CSV format
            df.to_csv(path_or_buf=response, index=False)

            return response
