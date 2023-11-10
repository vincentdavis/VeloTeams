# sync.py
import logging
import time
from json import JSONDecodeError

from django.db.models.base import ModelBase

from apps.teams.models import Team
from apps.zp.fetch import ZPSession
from apps.zp.models import Profile, TeamPending, TeamResults, TeamRiders


def create_or_update_model(self, zp_id, api, data_set):
    # Create a dictionary with dynamic field names
    kwargs = {
        "zp_id": zp_id,
        api: data_set,  # 'api' is the variable field name
    }

    # Unpack kwargs as arguments to get_or_create
    obj, created = self.model.objects.get_or_create(**kwargs)

    return obj, created


class FetchJsonRecords:
    """
    This adds a new json dataset to the model for each zp_id. It does not update any existing records.
    """

    def __init__(self, api: str, zp_id: int | list | str, model: ModelBase):
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
                    obj, created = self.model.objects.create_or_update_model({zp_id: zp_id, self.api: data_set})
                    logging.info(f"Created new {self.model} entry: {created} for team: {zp_id}")
            except JSONDecodeError as e:
                self.try_count += 1
                logging.warning(f"Retry get {self.api} number {self.try_count} data: {zp_id}")
                logging.warning(f"{e}")
            except Exception as e:
                self.try_count += 1
                logging.warning(f"Failed to get data: {e}")
                logging.warning(f"Retry get {self.api} number {self.try_count} data: {zp_id}")
            if self.try_count >= 4:
                logging.error(f"to many retries: {self.api} data: {zp_id}")
                break
            time.sleep(5 + self.try_count * 5)


class FetchTeamResults(FetchJsonRecords):
    def __init__(self):
        super().__init__(api="team_results", zp_id=Team.objects.values_list("zp_id", flat=True), model=TeamResults)


class FetchTeamPending(FetchJsonRecords):
    def __init__(self):
        super().__init__(api="team_pending", zp_id=Team.objects.values_list("zp_id", flat=True), model=TeamPending)


class FetchTeamRiders(FetchJsonRecords):
    def __init__(self):
        super().__init__(api="team_riders", zp_id=Team.objects.values_list("zp_id", flat=True), model=TeamRiders)


class UpdateJsonRecords:
    """
    This adds a UPDATES a json dataset in a model object.
    """

    def __init__(self, api: str, zp_id: int | list | str, model: ModelBase):
        self.zps = ZPSession()
        self.try_count = 0
        self.api = api
        self.zp_id = zp_id
        self.model = model

    def update(self):
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
                    obj, created = self.model.objects.create_or_update(zp_id=zp_id)
                    if created:
                        logging.info(f"Created new {self.model} entry: {created} for team: {zp_id}")
                        obj[self.api] = data_set
                        obj.save()
                    else:
                        logging.info(f"Updated {self.model} entry: {created} for team: {zp_id}")
                        obj[self.api] = data_set
                        obj.save()
                    logging.info(f"Created new {self.model} entry: {created} for team: {zp_id}")
            except JSONDecodeError as e:
                self.try_count += 1
                logging.warning(f"Retry get {self.api} number {self.try_count} data: {zp_id}")
                logging.warning(f"{e}")
            except Exception as e:
                self.try_count += 1
                logging.warning(f"Failed to get data: {e}")
                logging.warning(f"Retry get {self.api} number {self.try_count} data: {zp_id}")
            if self.try_count >= 4:
                logging.error(f"to many retries: {self.api} data: {zp_id}")
                break
            time.sleep(5 + self.try_count * 5)


class UpdateProfile(UpdateJsonRecords):
    def __init__(self):
        super().__init__(api="profile_profile", zp_id=Profile.objects.values_list("zp_id", flat=True), model=Profile)


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
