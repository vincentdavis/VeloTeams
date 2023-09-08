from django.db import models


class Profile(models.Model):
    """
    - profile:
    """

    id = models.IntegerField(blank=False, unique=True)
    profile = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # history = HistoricalRecords()


class Club(models.Model):
    """
    - Club:
    """

    id = models.IntegerField(blank=False, unique=True)
    profile = models.JSONField(blank=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # history = HistoricalRecords()
