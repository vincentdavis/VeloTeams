from datetime import datetime

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

    default_status = dict(
        last_event=0,  # Number of days since last event
        needs_update=True,  # Set for example becuase profile id is in an event result
        sorted=False,  # is the list of results sorted by date, recent to oldest, background task for this.
    )

    zp_id = models.IntegerField(blank=False, null=False, unique=True, db_index=True)
    profile = models.JSONField(blank=False, null=True)
    status = models.JSONField(blank=False, null=True, default=default_status)
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
        else:
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
        """
        Team name from most recent event
        """

        if self.profile:
            try:
                return f"{self.profile[0].get('tname', '-')}"
            except:
                return "-"
        else:
            return "-"

    def last_event(self):
        if self.profile:
            try:
                tstamp = self.profile[0].get("event_date")
                return datetime.fromtimestamp(tstamp).date()
            except:
                return "-"
        else:
            return "-"

    @property
    def recent_events(self):
        if self.profile:
            recent = []
            try:
                for event in self.profile[:3]:
                    event = {}
                    tstamp = event.get("event_date")
                    event["event_date"] = datetime.fromtimestamp(tstamp).date()
                    event["event_title"] = event.get("event_title")
                    event["team"] = event.get("tname")
                    event["url_event"] = f"{ZP_URL}/events.php?zid={event.get('zid')}"
                    recent.append(event)
                return recent
            except:
                return "-"
        else:
            return "-"

    @property
    def other_team_date(self):
        def recent_events(self):
            if self.profile:
                recent = []
                try:
                    for event in self.profile[:3]:
                        tstamp = event.get("event_date")
                        recent.append(datetime.fromtimestamp(tstamp).date(), event.get("tname"))
                    return recent
                except:
                    return [("-", "-")]
            else:
                return [("-", "-")]


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
    This is a list of events with results, not the actual results
    """

    event = models.JSONField(blank=False, null=True)
    zp_id = models.IntegerField(blank=False, null=False, unique=True)
    errors = models.CharField(max_length=255, blank=True, default="")
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
