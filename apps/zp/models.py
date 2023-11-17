from datetime import date, datetime, timedelta

from django.db import models
from django.utils.html import format_html

from config.settings.base import ZP_URL


class TeamRiders(models.Model):
    """
    - team_riders: /api3.php?do=team_riders&id={id}
    team_riders is the data stored as the list in "data":[....]
    """

    zp_id = models.IntegerField(blank=False, null=False)
    team_riders = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # history = HistoricalRecords()

    @property
    def rider_ids(self):
        try:
            return {rider.get("zwid", "") for rider in self.team_riders}
        except:
            return None


class TeamPending(models.Model):
    """
    - team_pending: /api3.php?do=team_pending&id={id}&_=1693775560118
    """

    zp_id = models.IntegerField(blank=False, null=False)
    team_pending = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # history = HistoricalRecords()


class TeamResults(models.Model):
    """
    - Results: /api3.php?do=team_results&id={id}
    """

    zp_id = models.IntegerField(blank=False, null=False)
    team_results = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    """
    - profile: /api3.php?do=profile&id={user_id}
    """

    zp_id = models.IntegerField(blank=False, null=False, unique=True, db_index=True)
    profile = models.JSONField(blank=False, null=True)
    error = models.CharField(max_length=255, blank=True, default="")
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # history = HistoricalRecords()
    @property
    def name(self):
        if self.profile:
            try:
                return f"{self.profile[0].get('name', '-')}"
            except:
                return "-"

    @property
    def url(self):
        """
        https://zwiftpower.com/events.php?zid=3896239
        """
        u = f"{ZP_URL}/profile.php?z={self.zp_id}"
        return format_html("<a href='{url}'>{url}</a>", url=u)

    @property
    def team(self):
        if self.profile:
            try:
                return f"{self.profile[0].get('tname', '-')}"
            except:
                return "-"

    def last_event(self):
        if self.profile:
            try:
                event_date = datetime.fromtimestamp(self.profile[0].get("event_date", "-")).date()
                return event_date
            except:
                return "-"

    @property
    def recent_teams(self):
        if self.profile:
            try:
                today_45 = date.today() - timedelta(days=45)
                current_team = self.profile[0].get("tname", "")  # get most recent team name
                recent_teams = []  # last 3
                print(f"current_team: {current_team}")
                for row in self.profile:
                    tname = row.get("tname", "")
                    event_date = datetime.fromtimestamp(row.get("event_date", "")).date()
                    print(f"tname: {tname} event_date: {event_date}")
                    if tname != current_team:
                        print(f"tname: {tname} event_date: {event_date}")
                    if tname != current_team and event_date > today_45:
                        recent_teams.append((tname, str(event_date)))
                        # print(f"recent_teams: {recent_teams}")
                    if len(recent_teams) >= 3 or event_date < today_45:
                        break
                return recent_teams if len(recent_teams) > 0 else None
            except:
                return None
            
    @property
    def other_team_date(self):
        # TODO : Vincent wokring on
        return "-"
    
class ProfileVictims(models.Model):
    """
    - profile_victims: /cache3/profile/{id}_rider_compare_victims.json
    """

    zp_id = models.IntegerField(blank=False, null=False)
    victims = models.JSONField(blank=False, null=True)
    error = models.CharField(max_length=255, blank=True, default="")
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProfileSignups(models.Model):
    """
    - profile_signups: /cache3/profile/{id}_signups.json
    """

    zp_id = models.IntegerField(blank=False, null=False)
    signups = models.JSONField(blank=False, null=True)
    error = models.CharField(max_length=255, blank=True, default="")
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AllResults(models.Model):
    """
    - /cache3/lists/0_zwift_event_list_results_3.json
    """

    results = models.JSONField(blank=False, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class EventResultsView(models.Model):
    """
    - /cache3/results/{id}_view.json
    """

    zp_id = models.IntegerField(blank=False, null=False, unique=True)
    results = models.JSONField(blank=False, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        """
        /events.php?zid=3896239
        """
        u = f"{ZP_URL}/events.php?zid={self.zp_id}"
        return format_html("<a href='{url}'>{url}</a>", url=u)


class EventResultsZwift(models.Model):
    """
    - /cache3/results/{id}_zwift.json
    """

    zp_id = models.IntegerField(blank=False, null=False, unique=True)
    results = models.JSONField(blank=False, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        """
        https://zwiftpower.com/events.php?zid=3896239
        """
        u = f"{ZP_URL}/events.php?zid={self.zp_id}"
        return format_html("<a href='{url}'>{url}</a>", url=u)


class Results(models.Model):
    """
    rows of results gathered from profiles
    """

    zp_id = models.IntegerField(blank=False, null=False, db_index=True)  # event_id
    zwid = models.IntegerField(blank=False, null=False, db_index=True)  # rider_id
    event_date = models.DateField(blank=False, null=False)  # event_date
    tid = models.IntegerField(blank=False, null=True)  # team_id
    team = models.CharField(max_length=255, blank=True, default="")  # tname
    name = models.CharField(max_length=255, blank=True, default="")  # name
    event_title = models.CharField(max_length=255, blank=True, default="")  # event_title
    results = models.JSONField(blank=False, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["zp_id", "zwid"], name="unique_zp_id_zwid"),
        ]

    def __str__(self):
        return f"{self.zp_id}, {self.zwid}, {self.event_date}"

    def url_event(self):
        """
        /events.php?zid=3896239
        """
        u = f"{ZP_URL}/events.php?zid={self.zp_id}"
        return u

    @property
    def url_profile(self):
        """
        /profile.php?z=3896239
        """
        u = f"{ZP_URL}/profile.php?z={self.zwid}"
        return u

    @property
    def url_event_link(self):
        """
        /events.php?zid=3896239
        """
        u = f"{ZP_URL}/events.php?zid={self.zp_id}"
        return format_html("<a href='{url}'>{url}</a>", url=u)

    def url_profile_link(self):
        """
        /profile.php?z=3896239
        """
        u = f"{ZP_URL}/profile.php?z={self.zwid}"
        return format_html("<a href='{url}'>{url}</a>", url=u)
