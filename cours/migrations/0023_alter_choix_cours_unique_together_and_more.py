# Generated by Django 4.2.5 on 2024-03-13 19:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0022_choix_cours_date_alter_choix_cours_cours"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="choix_cours",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="choix_cours",
            name="date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
