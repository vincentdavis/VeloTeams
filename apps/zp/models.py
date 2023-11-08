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

    team_pending = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # history = HistoricalRecords()


class TeamResults(models.Model):
    """
    - Results: /api3.php?do=team_results&id={id}
    """

    team_results = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    """
    - profile: /api3.php?do=profile&id={user_id}
    """

    zp_id = models.IntegerField(blank=False, null=False)
    profile = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # history = HistoricalRecords()


class ProfileVictims(models.Model):
    """
    - profile_victims: /cache3/profile/{id}_rider_compare_victims.json
    """

    victims = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProfileSignups(models.Model):
    """
    - profile_signups: /cache3/profile/{id}_signups.json
    """

    signups = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
