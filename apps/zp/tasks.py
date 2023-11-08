import time
from config import celery_app
from .sync import TeamRidersUpdater, ProfilesFromTeams, ZPProfileUpdater

@celery_app.task()
def update_teamriders_task():
    updater = TeamRidersUpdater()
    updater.update_teamriders()


@celery_app.task()
def add_profiles_from_teams_task():
    profile_adder = ProfilesFromTeams()
    profile_adder.add_profiles_from_teams()


@celery_app.task()
def update_zp_profiles_task():
    profile_updater = ZPProfileUpdater()
    profile_updater.update_profiles()