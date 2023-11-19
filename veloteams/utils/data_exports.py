import csv
import logging
from datetime import date, timedelta

import pandas as pd
from django.contrib import messages
from django.http import HttpResponse

from apps.zp.models import Results, TeamRiders
from config.settings.base import ZP_URL


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


def zp_teamrider_results_to_csv(modeladmin, request, queryset, latest=3):
    if queryset.count() > 1:
        messages.warning(request, "This action can only be performed on a single item at a time.")
        return

    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={opts}.csv"

    def blank_row(rider_id):
        rider_result = {"on_team_ids": rider_id}
        rider_result.update(
            {
                "event_date": "-",
                "zp_id": "-",
                "event_title": "-",
                "url_event": "-",
                "name": "-",
                "url_profile": f"{ZP_URL}/profile.php?z={rider_id}",
                "team": "-",
                "tid": "-",
                "Recent_Teams": "-",
            }
        )
        writer.writerow(rider_result)

    rider_ids = queryset[0].rider_ids
    columns = [
        "on_team_ids",
        "event_date",
        "zp_id",
        "event_title",
        "url_event",
        "zwid",
        "name",
        "url_profile",
        "team",
        "tid",
        "Recent_Teams",
    ]
    writer = csv.DictWriter(response, fieldnames=columns)
    db_fields = [field for field in columns if field not in ["on_team_ids", "Recent_Teams"]]
    writer.writeheader()
    # team_rider_results = []
    days = date.today() - timedelta(days=60)
    for rider_id in rider_ids:
        try:
            results = Results.objects.filter(zwid=rider_id, event_date__gte=days).order_by("-event_date")[:3]
            # print(results)
            if results.count() > 0:
                rider_result = {"Recent_Teams": set(), "on_team_ids": rider_id}
                # print(results[0])
                for field in db_fields:
                    value = getattr(results[0], field, "-")
                    if callable(value):
                        value = value()
                    rider_result[field] = value
                for result in results:
                    try:
                        rider_result["Recent_Teams"].add(result.team)
                    except Exception as e:
                        logging.error(f"failed to get team: result_id: {result.id}\n {e}")
                writer.writerow(rider_result)
            else:
                logging.warning(f"results<0: {results}")
                blank_row(rider_id)
        except Exception as e:
            logging.error(f"Failed to export {rider_id}\n {e}")
            blank_row(rider_id)
    return response


def teamriderreport(zp_id: int = None, queryset=None, days: int = 180):
    if queryset is None:
        queryset = TeamRiders.objects.filter(zp_id=zp_id).order_by("-created_at")[0]
    rider_ids = queryset[0].rider_ids  # rider_ids is a property
    df_rider_ids = pd.DataFrame(rider_ids, columns=["zwid"])
    data = (
        Results.objects.filter(zwid__in=rider_ids, event_date__gte=date.today() - timedelta(days=180))
        .order_by("-event_date")
        .values()
    )
    df = pd.DataFrame(data)
    df = df.sort_values(by="event_date", ascending=False)  # it should already be sorted
    df_most_recent = df.groupby("zwid").head(1).reset_index()
    df_recent = df.groupby("zwid").head(3).reset_index().groupby("zwid")["team"].unique().reset_index()
    df_recent.rename(columns={"team": "recent_teams"}, inplace=True)
    df = pd.merge(df_most_recent, df_recent, on="zwid", how="left")
    df = pd.merge(df_rider_ids, df, on="zwid", how="left")
    df.sort_values("event_date", ascending=False, inplace=True)
    df["URL"] = df["zwid"].apply(lambda x: f"https://www.zwiftpower.com/profile.php?z={x}")
    df.reset_index(inplace=True, drop=True)
    return df[["zwid", "name", "team", "recent_teams", "event_date", "URL"]]


def teamrider_report_csv(modeladmin, request, queryset):
    """This is to be used on the TeamRiders modeladmin page. Select 1"""
    if queryset.count() > 1:
        messages.warning(request, "This action can only be performed on a single item at a time.")
        return
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=TeamRidersReport.csv"
    teamriderreport(queryset=queryset).to_csv(path_or_buf=response, index=False)
    return response
