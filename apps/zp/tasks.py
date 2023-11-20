from config import celery_app

from .sync import (
    FetchAllResults,
    FetchTeamPending,
    FetchTeamResults,
    FetchTeamRiders,
    ProfilesFromTeams,
    ResultsFromProfiles,
    SetLastEventProfile,
    UpdateProfileErrors,
    UpdateProfiles,
)


@celery_app.task(soft_time_limit=250)
def fetch_teamriders_task(soft_time_limit=250):
    action = FetchTeamRiders()
    action.fetch()


@celery_app.task(soft_time_limit=250)
def fetch_teamresults_task(soft_time_limit=250):
    action = FetchTeamResults()
    action.fetch()


@celery_app.task()
def fetch_teampending_tasks(soft_time_limit=250):
    action = FetchTeamPending()
    action.fetch()


@celery_app.task(soft_time_limit=250)
def add_profiles_from_teams_task():
    profile_adder = ProfilesFromTeams()
    profile_adder.update()


@celery_app.task(soft_time_limit=500)
def update_profiles_task():
    action = UpdateProfiles()
    action.update()


@celery_app.task(soft_time_limit=500)
def update_profile_errors():
    action = UpdateProfileErrors()
    action.update()


@celery_app.task(soft_time_limit=60)
def fetch_allresults():
    action = FetchAllResults()
    action.fetch()


@celery_app.task(soft_time_limit=600)
def results_from_profiles():
    action = ResultsFromProfiles()
    action.update()


@celery_app.task(soft_time_limit=500)
def lastEventprofileset():
    action = SetLastEventProfile()
    action.update()
