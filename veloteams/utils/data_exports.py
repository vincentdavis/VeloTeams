import csv
import logging

from django.contrib import messages
from django.http import HttpResponse

from apps.zp.models import Results
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
        "Recent_Teams",
    ]
    writer = csv.DictWriter(response, fieldnames=columns)
    db_fields = [field for field in columns if field not in ["on_team_ids", "Recent_Teams"]]
    writer.writeheader()
    # team_rider_results = []
    for rider_id in rider_ids:
        # print(rider_id)
        results = Results.objects.filter(zwid=rider_id).order_by("-event_date")[:3]
        # print(results)
        if results.count() > 0:
            rider_result = {"Recent_Teams": set(), "on_team_ids": rider_id}
            print(results[0])
            for field in db_fields:
                value = getattr(results[0], field, "")
                if callable(value):
                    value = value()
                rider_result[field] = value
            for result in results:
                rider_result["Recent_Teams"].add(result.team)
            writer.writerow(rider_result)
        else:
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
                }
            )
            # team_rider_results.append(my_object_dict)
            writer.writerow(rider_result)
    return response
