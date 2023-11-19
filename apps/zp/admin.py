from django.contrib import admin

from veloteams.utils.data_exports import model_to_csv, teamrider_report_csv

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


def profiles_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    # Write a first row with header information
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many and field.name != "profile"
    ]
    properties = ["team", "last_event"]
    return model_to_csv(modeladmin, request, queryset, fields, properties, json_field=None)


profiles_to_csv.short_description = "Export to CSV"


def teamriders_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    # Write a first row with header information
    return model_to_csv(modeladmin, request, queryset[0], fields=[], properties=[], json_field="team_riders")


teamrider_report_csv.short_description = "Export teamriders to CSV"


# Register your models here.
@admin.register(TeamRiders)
class TeamRidersAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]
    actions = [teamrider_report_csv]


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
    list_per_page = 100
    list_display = ["id", "zp_id", "name", "team", "last_event", "url", "error", "modified_at", "created_at"]
    list_filter = ["error", "modified_at", "created_at"]
    search_fields = ["zp_id"]
    actions = [update_selected_profiles, profiles_to_csv]


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
    list_display = [
        "id",
        "zp_id",
        "zwid",
        "name",
        "team",
        "url_event_link",
        "url_profile_link",
        "event_date",
        "modified_at",
        "created_at",
    ]
    search_fields = ["zp_id", "zwid", "name", "team"]
    list_filter = ["event_date", "modified_at", "created_at"]
