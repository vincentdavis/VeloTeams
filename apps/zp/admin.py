from django.contrib import admin

from .models import (
    AllResults,
    EventResultsView,
    EventResultsZwift,
    Profile,
    ProfileSignups,
    ProfileVictims,
    TeamPending,
    TeamResults,
    TeamRiders,
)


# Register your models here.
@admin.register(TeamRiders)
class TeamRidersAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]


@admin.register(TeamPending)
class TeamPendingAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]


@admin.register(TeamResults)
class TeamResultsAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]


@admin.register(ProfileVictims)
class ProfileVictimsAdmin(admin.ModelAdmin):
    list_display = ["modified_at", "created_at"]


@admin.register(ProfileSignups)
class ProfileSignupsAdmin(admin.ModelAdmin):
    list_display = ["modified_at", "created_at"]


@admin.register(AllResults)
class AllResultsAdmin(admin.ModelAdmin):
    list_display = ["modified_at", "created_at"]


@admin.register(EventResultsView)
class EventResultsViewAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]


@admin.register(EventResultsZwift)
class EventResultsZwiftAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]
