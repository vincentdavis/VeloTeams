from django.core.management.base import BaseCommand

from apps.zp.sync import FetchTeamResults


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        """Get a list of zp team ids and fetch the member list"""
        updater = FetchTeamResults()
        updater.fetch()
