# Generated by Django 4.1.1 on 2022-10-10 12:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("matchs", "0003_alter_match_match_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="match_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(null=True), null=True, size=None
                    ),
                    null=True,
                    size=None,
                ),
                null=True,
                size=None,
            ),
        ),
    ]