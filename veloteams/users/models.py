from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ForeignKey, SET_NULL
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from zp.models import Profile as ZPProfile
from zw.models import Profile as ZWProfile


class User(AbstractUser):
    """
    Default custom user model for VeloTeams2.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    zp_id = ForeignKey(ZPProfile, on_delete=SET_NULL, null=True, unique=True)  # user ID at zp
    zw_id = ForeignKey(ZWProfile, on_delete=SET_NULL, null=True, unique=True)  # user ID at zw

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
