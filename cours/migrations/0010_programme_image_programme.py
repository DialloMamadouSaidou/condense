# Generated by Django 4.2.5 on 2024-02-19 16:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0009_note_commentaire"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="image_programme",
            field=models.ImageField(blank=True, upload_to="image/programme"),
        ),
    ]
