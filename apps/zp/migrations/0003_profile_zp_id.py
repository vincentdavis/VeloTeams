# Generated by Django 4.2.6 on 2023-11-03 03:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zp", "0002_teamriders_zp_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="zp_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]