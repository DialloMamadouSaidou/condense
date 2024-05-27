# Generated by Django 4.2.5 on 2024-05-22 02:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0009_rename_paie_profile_pai"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="pai",
        ),
        migrations.AddField(
            model_name="profile",
            name="code_secret",
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
