# Generated by Django 4.1.1 on 2022-10-21 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("matchs", "0012_match_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
