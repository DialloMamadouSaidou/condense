# Generated by Django 4.2.5 on 2024-02-19 14:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0008_alter_chapitre_identifiant"),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="commentaire",
            field=models.CharField(default="bon eleve", max_length=500),
        ),
    ]
