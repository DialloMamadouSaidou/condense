# Generated by Django 4.2.5 on 2024-03-13 20:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0008_profile_paie"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="paie",
            new_name="pai",
        ),
    ]
