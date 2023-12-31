# Generated by Django 4.2.6 on 2023-11-02 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("zp", "0001_initial"),
        ("teams", "0002_alter_teammember_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="results",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="zp.teamresults",
                verbose_name="Zwift ID",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="zp_id",
            field=models.IntegerField(
                blank=True, unique=True, verbose_name="Zwift Power ID"
            ),
        ),
    ]
