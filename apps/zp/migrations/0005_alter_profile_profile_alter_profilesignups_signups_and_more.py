# Generated by Django 4.2.7 on 2023-11-09 03:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zp", "0004_profilesignups_zp_id_profilevictims_zp_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="profilesignups",
            name="signups",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="profilevictims",
            name="victims",
            field=models.JSONField(null=True),
        ),
    ]
