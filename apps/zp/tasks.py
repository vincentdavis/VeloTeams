from fetch import ZPSession

from config import celery_app


@celery_app.task()
def update_team_rosters():
    """Get a list of zp team ids and fetch the member list"""
    zps = ZPSession()
    data_set = zps.get_api(id=11991, api="team_riders")
    return data_set
