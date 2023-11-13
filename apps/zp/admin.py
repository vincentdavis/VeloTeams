from django.contrib import admin

from .models import (
    AllResults,
    EventResultsView,
    EventResultsZwift,
    Profile,
    ProfileSignups,
    ProfileVictims,
    Results,
    TeamPending,
    TeamResults,
    TeamRiders,
)
from .sync import UpdateSelected


def update_selected_profiles(modeladmin, request, queryset):
    api = "profile_profile"
    zp_id = list(queryset.values_list("zp_id", flat=True))
    model = Profile
    u = UpdateSelected(api=api, zp_id=zp_id, model=model)
    u.update()


update_selected_profiles.short_description = "Update selected profiles"


# Register your models here.
@admin.register(TeamRiders)
class TeamRidersAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(TeamPending)
class TeamPendingAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(TeamResults)
class TeamResultsAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "name", "url", "error", "modified_at", "created_at"]
    list_filter = ["error", "modified_at", "created_at"]
    search_fields = ["zp_id"]
    actions = [update_selected_profiles]


@admin.register(ProfileVictims)
class ProfileVictimsAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "error", "modified_at", "created_at"]
    list_filter = ["error", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(ProfileSignups)
class ProfileSignupsAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "error", "modified_at", "created_at"]
    list_filter = ["error", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(AllResults)
class AllResultsAdmin(admin.ModelAdmin):
    list_display = ["id", "modified_at", "created_at"]
    list_filter = ["modified_at", "created_at"]


@admin.register(EventResultsView)
class EventResultsViewAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "url", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(EventResultsZwift)
class EventResultsZwiftAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "url", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "zwid", "name", "team", "url", "event_date", "modified_at", "created_at"]
    search_fields = ["zp_id", "zwid", "name", "team"]
    list_filter = ["event_date", "modified_at", "created_at"]
