# Generated by Django 4.2.5 on 2024-02-07 05:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_alter_myuser_managers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="identifiant",
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]
