from django.contrib.auth import get_user_model
from django.db import models

from zp.models import Profile as ZPProfile
from zp.models import TeamPending
from zp.models import TeamResults
from zp.models import TeamRiders
from zw.models import Club
from zw.models import Profile as ZWProfile

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
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    zp_id = models.ForeignKey(ZPProfile, on_delete=models.SET_NULL, null=True)  # user ID at zp
    zw_id = models.ForeignKey(ZWProfile, on_delete=models.SET_NULL, null=True)  # user ID at zw
    is_owner = models.BooleanField(default=False)  # is team super admin/owner
    is_admin = models.BooleanField(default=False)  # is team admin
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
