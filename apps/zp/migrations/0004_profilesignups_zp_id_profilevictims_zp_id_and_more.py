# Generated by Django 4.2.7 on 2023-11-09 03:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zp", "0003_profile_zp_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="profilesignups",
            name="zp_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="profilevictims",
            name="zp_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="teampending",
            name="zp_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="teamresults",
            name="zp_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]