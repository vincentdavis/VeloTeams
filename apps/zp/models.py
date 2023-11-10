from django.db import models


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

    zp_id = models.IntegerField(blank=False, null=False, unique=True)
    profile = models.JSONField(blank=False, null=True)
    error = models.CharField(max_length=255, blank=True, default="")
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # history = HistoricalRecords()


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


class EventResultsZwift(models.Model):
    """
    - /cache3/results/{id}_zwift.json
    """

    zp_id = models.IntegerField(blank=False, null=False, unique=True)
    results = models.JSONField(blank=False, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
