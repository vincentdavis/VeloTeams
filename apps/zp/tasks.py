from config import celery_app

from .sync import FetchTeamPending, FetchTeamResults, FetchTeamRiders, ProfilesFromTeams, ZPProfileUpdater


@celery_app.task()
def fetch_teamriders_task():
    action = FetchTeamRiders()
    action.fetch()


@celery_app.task()
def fetch_teamresults_task():
    action = FetchTeamResults()
    action.fetch()


@celery_app.task()
def fetch_teampending_tasks():
    action = FetchTeamPending()
    action.fetch()


@celery_app.task()
def add_profiles_from_teams_task():
    profile_adder = ProfilesFromTeams()
    profile_adder.add_profiles_from_teams()


@celery_app.task()
def update_zp_profiles_task():
    profile_updater = ZPProfileUpdater()
    profile_updater.update_profiles()
