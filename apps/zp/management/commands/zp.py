from django.core.management.base import BaseCommand

from apps.zp.models import Profile
from apps.zp.sync import FetchTeamResults, ProfilesFromTeams, ResultsFromProfiles, UpdateProfileErrors, UpdateProfiles


class TeamRiders(BaseCommand):
    help = "Fetch Team Riders for all teams"

    def handle(self, *args, **options):
        """Get a list of zp team ids and fetch the member list"""
        self.stdout.write(self.style.SUCCESS("Fetch Team Riders: Start"))
        updater = FetchTeamResults()
        updater.fetch()
        self.stdout.write(self.style.SUCCESS("Fetch Team Riders: Done"))


class TeamResults(BaseCommand):
    help = "Fetch Team Results for all teams"

    def handle(self, *args, **options):
        """Get a list of zp team ids and fetch the member list"""
        self.stdout.write(self.style.SUCCESS("Fetch Team Results: Start"))
        updater = FetchTeamResults()
        updater.fetch()
        self.stdout.write(self.style.SUCCESS("Fetch Team Results: Done"))


class ProfilesUpdate(BaseCommand):
    help = "Update the oldest `count` number of Profiles"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10)

    def handle(self, *args, **options):
        count = options["count"]
        action = UpdateProfiles()
        action.zp_id = Profile.objects.filter(error="").order_by("modified_at").values_list("zp_id", flat=True)[:count]
        action.update()


class ProfilesErrors(BaseCommand):
    help = "Try to update profiles with errors"

    def handle(self, *args, **options):
        action = UpdateProfileErrors()
        action.update()


class ProfilesTeams(BaseCommand):
    help = "Create profiles from teamsriders model"

    def handle(self, *args, **options):
        """Get a list of zp team ids and fetch the member list"""
        f = ProfilesFromTeams()
        f.update()


class ProfilesToResults(BaseCommand):
    help = "Create results from profiles"

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=60)

    def handle(self, *args, **options):
        """Get a list of zp team ids and fetch the member list"""
        days = options["days"]
        f = ResultsFromProfiles(days=days)
        f.update()
