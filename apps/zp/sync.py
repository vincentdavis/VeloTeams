# sync.py
import logging
import time

from apps.teams.models import Team
from apps.zp.fetch import ZPSession
from apps.zp.models import Profile, TeamPending, TeamResults, TeamRiders


class fetch_json_records:
    """
    This adds a new json dataset to the model for each zp_id. It does not update any existing records.
    """

    def __init__(self, api: str, zp_id: int | list | str = None, model: object = None):
        self.zps = ZPSession()
        self.try_count = 0
        self.api = api
        self.zp_id = zp_id
        self.model = model

    def fetch(self):
        if isinstance(self.zp_id, int | list):
            zp_ids = set(self.zp_id)
        elif isinstance(self.zp_id, str) and self.zp_id == "all":
            zp_ids = set(self.model.objects.values_list("zp_id", flat=True))
            logging.info(f"zp_id count: {len(zp_ids)}")
        else:
            raise ValueError("zp_id must be int, list, or 'all'")
        for zp_id in zp_ids:
            logging.info(f"Get {self.api} data: {zp_id}")
            try:
                data_set = self.zps.get_api(id=zp_id, api=self.api)[self.api]
                if "data" in data_set:
                    data_set = data_set["data"]
                if len(data_set) > 0:
                    tr, created = self.model.objects.get_or_create(zp_id=zp_id, team_riders=data_set)
                    logging.info(f"Created new {self.model} entry: {created} for team: {zp_id}")
            except Exception as e:
                self.try_count += 1
                logging.warning(f"Failed to get data: {e}")
                logging.warning(f"Retry get {self.api} number {self.try_count} data: {zp_id}")
                if self.try_count >= 4:
                    logging.error(f"to many retries: {self.api} data: {zp_id}")
                    break
            time.sleep(5 + self.try_count * 30)


class FetchTeamPending(fetch_json_records):
    def __init__(self):
        super().__init__(api="team_pending", zp_id=Team.objects.values_list("zp_id", flat=True), model=TeamPending)


class FetchTeamRiders:
    def __init__(self):
        self.zps = ZPSession()
        self.try_count = 0

    def fetch(self):
        zp_team_ids = Team.objects.values_list("zp_id", flat=True)
        for zp_team_id in zp_team_ids:
            logging.info(f"Get team data: {zp_team_id}")
            try:
                data_set = self.zps.get_api(id=zp_team_id, api="team_riders")
                data_set = data_set["team_riders"]["data"]
                if len(data_set) > 0:
                    tr, created = TeamRiders.objects.get_or_create(zp_id=zp_team_id, team_riders=data_set)
                    logging.info(f"Created new TeamRider entry: {created} for team: {zp_team_id}")
            except Exception as e:
                self.try_count += 1
                logging.warning(f"Failed to get team data: {e}")
                logging.warning(f"Retry get team data: {zp_team_id}")
                if self.try_count >= 4:
                    logging.error(f"Retry get team data: {zp_team_id}")
                    break
            time.sleep(5 + self.try_count * 30)


class FetchTeamResults:
    def __init__(self):
        self.zps = ZPSession()
        self.try_count = 0

    def fetch(self):
        zp_team_ids = Team.objects.values_list("zp_id", flat=True)
        for zp_team_id in zp_team_ids:
            logging.info(f"Get team result data: {zp_team_id}")
            try:
                data_set = self.zps.get_api(id=zp_team_id, api="team_results")
                data_set = data_set["team_results"]  # dict_keys(['events', 'data'])
                if "events" in data_set and " in data_set":
                    tr, created = TeamResults.objects.get_or_create(zp_id=zp_team_id, team_results=data_set)
                    logging.info(f"Created new TeamResult entry: {created} for team: {zp_team_id}")

            except Exception as e:
                self.try_count += 1
                logging.warning(f"Failed to get team result data: {e}")
                logging.info(f"Retry get team result data: {zp_team_id}")
                if self.try_count >= 4:
                    logging.error(f"Exceeded get team result data : {zp_team_id}")
                    break
            time.sleep(5 + self.try_count * 30)


class ProfilesFromTeams:
    def add_profiles_from_teams(self):
        logging.info("Move profiles from teams to profiles table")
        # zp_team_riders = TeamRiders.objects.all()
        zp_team_riders = TeamRiders.objects.order_by("zp_id", "-modified_at").distinct("zp_id")
        for team in zp_team_riders:
            logging.info(f"Adding profiles from team: {team.zp_id}")
            for rider in team.team_riders:
                logging.info(f"Get or creat zp Profile: {rider['zwid']}")
                got, created = Profile.objects.get_or_create(zp_id=int(rider["zwid"]))
                logging.info(f"Created? {created} rider Profile{rider['zwid']}")


class ZPProfileUpdater:
    def __init__(self):
        self.zps = ZPSession()
        self.try_count = 0

    def update_profiles(self):
        # zp_profiles = Profile.objects.all()
        oldest_profiles = Profile.objects.order_by("modified_at")[:50]
        for zp_profile in oldest_profiles:
            try:
                data_set = self.zps.get_api(id=zp_profile.zp_id, api="profile_profile")
                data_set = data_set["profile_profile"]["data"]
                if len(data_set) > 0:
                    zp_profile.profile = data_set
                    zp_profile.save()
            except:
                self.try_count += 1
            if self.try_count >= 4:
                break
            time.sleep(5 + self.try_count * 30)
