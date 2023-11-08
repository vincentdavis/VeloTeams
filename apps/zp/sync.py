# sync.py

import time
from apps.zp.fetch import ZPSession
from apps.zp.models import Profile, TeamRiders

class TeamRidersUpdater:
    def __init__(self):
        self.zps = ZPSession()
        self.try_count = 0

    def update_teamriders(self):
        zp_team_ids = TeamRiders.objects.values_list("zp_id", flat=True)
        for zp_team_id in zp_team_ids:
            try:
                data_set = self.zps.get_api(id=zp_team_id, api="team_riders")
                if len(data_set) > 0:
                    team_obj = TeamRiders.objects.get(zp_id=zp_team_id)
                    team_obj.team_riders = data_set
                    team_obj.save()
            except:
                self.try_count += 1
            if self.try_count >= 4:
                break
            time.sleep(5 + self.try_count * 30)


class ProfilesFromTeams:
    def add_profiles_from_teams(self):
        zp_team_riders = TeamRiders.objects.all()
        for team in zp_team_riders:
            for rider in team.team_riders:
                Profile.objects.get_or_create(zp_id=rider["zwid"])


class ZPProfileUpdater:
    def __init__(self):
        self.zps = ZPSession()
        self.try_count = 0

    def update_profiles(self):
        zp_profiles = Profile.objects.all()
        for zp_profile in zp_profiles:
            try:
                data_set = self.zps.get_api(id=zp_profile.zp_id, api="profile_profile")
                if len(data_set) > 0:
                    zp_profile.profile = data_set
                    zp_profile.save()
            except:
                self.try_count += 1
            if self.try_count >= 4:
                break
            time.sleep(5 + self.try_count * 30)
