# Generated by Django 4.2.5 on 2024-02-17 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="module",
            name="chapitre",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cours.chapitre",
            ),
        ),
    ]
