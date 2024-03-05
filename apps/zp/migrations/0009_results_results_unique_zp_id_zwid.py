# Generated by Django 4.2.7 on 2023-11-11 03:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zp", "0008_profile_error_profilesignups_error_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Results",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("zp_id", models.IntegerField()),
                ("zwid", models.IntegerField()),
                ("event_date", models.DateField()),
                ("team", models.CharField(blank=True, default="", max_length=255)),
                ("name", models.CharField(blank=True, default="", max_length=255)),
                ("results", models.JSONField(null=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name="results",
            constraint=models.UniqueConstraint(fields=("zp_id", "zwid"), name="unique_zp_id_zwid"),
        ),
    ]
