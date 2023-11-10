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
    search_fields = ["zp_id"]


@admin.register(TeamPending)
class TeamPendingAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(TeamResults)
class TeamResultsAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "error", "modified_at", "created_at"]
    list_filter = ["error", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(ProfileVictims)
class ProfileVictimsAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "error", "modified_at", "created_at"]
    list_filter = ["error", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(ProfileSignups)
class ProfileSignupsAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "error", "modified_at", "created_at"]
    list_filter = ["error", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(AllResults)
class AllResultsAdmin(admin.ModelAdmin):
    list_display = ["modified_at", "created_at"]
    list_filter = ["modified_at", "created_at"]


@admin.register(EventResultsView)
class EventResultsViewAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]


@admin.register(EventResultsZwift)
class EventResultsZwiftAdmin(admin.ModelAdmin):
    list_display = ["zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]
