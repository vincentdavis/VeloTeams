from django.contrib.auth import get_user_model
from django.db import models

from apps.zp.models import TeamRiders

User = get_user_model()


# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=255, blank=False)
    zp_id = models.IntegerField(blank=True, null=True, unique=True, verbose_name="Zwift Power ID")  # team ID at zp
    zw_id = models.CharField(
        blank=True, unique=True, verbose_name="Zwift Club Name", default=""
    )  # Club name at Zwift.com)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.team_name

    @property
    def zwift_riders(self):
        try:
            # Get the latest TeamRiders object for this profile based on the created_at field
            return TeamRiders.objects.filter(zp_id=self.zp_id).latest("created_at")
        except TeamRiders.DoesNotExist:
            # If no TeamRiders object is found, return None or handle as appropriate
            return None


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
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PENDING)  # status of the user in the team
    is_owner = models.BooleanField(default=False)  # is team super admin/owner
    is_admin = models.BooleanField(default=False)  # is team admin
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
