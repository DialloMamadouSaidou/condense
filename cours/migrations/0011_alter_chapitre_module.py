# Generated by Django 4.2.5 on 2024-02-19 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0010_programme_image_programme"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chapitre",
            name="module",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cours.module",
            ),
        ),
    ]
