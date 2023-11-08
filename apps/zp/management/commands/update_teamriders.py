from django.core.management.base import BaseCommand
from apps.zp.fetch import ZPSession
from apps.zp.models import Profile, TeamRiders
import time
from apps.zp.sync import TeamRidersUpdater, ProfilesFromTeams, ZPProfileUpdater


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        """Get a list of zp team ids and fetch the member list"""
        updater = TeamRidersUpdater()
        updater.update_teamriders()

