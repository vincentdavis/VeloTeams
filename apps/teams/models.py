from django.contrib.auth import get_user_model
from django.db import models

from apps.zp.models import Profile as ZPProfile
from apps.zp.models import TeamPending
from apps.zp.models import TeamResults
from apps.zp.models import TeamRiders
from apps.zw.models import Club
from apps.zw.models import Profile as ZWProfile

User = get_user_model()


# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=255, blank=False)
    zp_id = models.IntegerField(blank=True, unique=True)  # team ID at zp
    riders = models.ForeignKey(TeamRiders, on_delete=models.SET_NULL, null=True)  # team ID at zp
    pending = models.ForeignKey(TeamPending, on_delete=models.SET_NULL, null=True)  # team ID at zp
    results = models.ForeignKey(TeamResults, on_delete=models.SET_NULL, null=True)  # team ID at zp
    zw_id = models.ForeignKey(ZWProfile, on_delete=models.SET_NULL, null=True)  # Club ID at zw
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TeamMember(models.Model):
    PENDING = "pending"
    PROCESSING = "processing"
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
        (SUSPENDED, "Suspended"),
    ]
    team = models.ManyToManyField(Team)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, unique=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PENDING)  # status of the user in the team
    is_owner = models.BooleanField(default=False)  # is team super admin/owner
    is_admin = models.BooleanField(default=False)  # is team admin
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
