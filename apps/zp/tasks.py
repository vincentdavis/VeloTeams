import time

from apps.zp.fetch import ZPSession
from apps.zp.models import Profile, TeamRiders
from config import celery_app


@celery_app.task()
def update_teamriders():
    """Get a list of zp team ids and fetch the member list"""
    zps = ZPSession()
    zp_team_ids = TeamRiders.objects.values_list("zp_id", flat=True)
    try_count = 0
    for zp_team_id in zp_team_ids:
        try:
            data_set = zps.get_api(id=zp_team_id, api="team_riders")
            if len(data_set) > 0:
                team_obj = TeamRiders(zp_id=zp_team_id, team_riders=data_set)
                team_obj.save()
        except:
            try_count += 1
        if try_count >= 4:  # if it keeps failing we want to backoff and then giveup
            break
        time.sleep(5 + try_count * 30)


@celery_app.task()
def add_profiles_from_teams():
    zp_team_riders = TeamRiders.objects.all()
    for team in zp_team_riders:
        for rider in team.team_riders:
            Profile.objects.get_or_create(zp_id=rider["zwid"])


@celery_app.task()
def zp_profile():
    zps = ZPSession()
    zp_profiles = Profile.objects.all()
    try_count = 0
    for zp_profile in zp_profiles:
        try:
            data_set = zps.get_api(id=zp_profile.zp_id, api="profile_profile")
            if len(data_set) > 0:
                zp_profile.profile = data_set
                zp_profile.save()
        except:
            try_count += 1
        if try_count >= 4:
            break
        time.sleep(5 + try_count * 30)
