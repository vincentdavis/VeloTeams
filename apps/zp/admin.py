import csv
import logging

from django.contrib import admin
from django.http import HttpResponse

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


def model_to_csv(modeladmin, request, queryset, fields=[], properties=[], json_field: str = None):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={opts}.csv"
    writer = csv.writer(response)
    if json_field is not None:
        logging.info("#### json_field ####")
        try:
            # print(getattr(queryset, json_field))
            header = list(getattr(queryset, json_field)[0].keys())
            writer.writerow(header)
            json_data = getattr(queryset, json_field)
            # print(f"data: {json_data[0]}")
            for row in json_data:
                # print(f"row: {row.values()}")
                writer.writerow(row.values())
        except Exception as e:
            logging.error(f"{e}")
    else:
        header = [f.name for f in fields] + properties
        writer.writerow(header)
        logging.info(f"CSV Header: {header}")
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if callable(value):
                    value = value()
                # if isinstance(value, str):
                #     value = value.encode("utf-8", "replace")
                data_row.append(value)
            for prop in properties:
                value = getattr(obj, prop)
                if callable(value):
                    value = value()
                # if isinstance(value, str):
                #     value = value.encode("utf-8", "replace")
                data_row.append(value)
            writer.writerow(data_row)
    return response


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
    # print(fields)
    properties = ["team", "recent_teams", "url"]
    return model_to_csv(modeladmin, request, queryset, fields, properties, json_field=None)


profiles_to_csv.short_description = "Export to CSV"


def teamriders_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    # Write a first row with header information
    return model_to_csv(modeladmin, request, queryset[0], fields=[], properties=[], json_field="team_riders")


teamriders_to_csv.short_description = "Export riders to CSV"


# Register your models here.
@admin.register(TeamRiders)
class TeamRidersAdmin(admin.ModelAdmin):
    list_display = ["id", "zp_id", "modified_at", "created_at"]
    search_fields = ["zp_id"]
    actions = [teamriders_to_csv]


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
    list_per_page = 500
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
    list_display = ["id", "zp_id", "zwid", "name", "team", "url", "event_date", "modified_at", "created_at"]
    search_fields = ["zp_id", "zwid", "name", "team"]
    list_filter = ["event_date", "modified_at", "created_at"]
