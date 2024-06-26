# Generated by Django 4.2.5 on 2024-04-01 21:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0009_rename_paie_profile_pai"),
        ("cours", "0026_payer"),
    ]

    operations = [
        migrations.AddField(
            model_name="payer",
            name="session",
            field=models.CharField(default="sessin hiver", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="payer",
            name="identifiant",
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="payer",
            unique_together={("module", "profile", "session")},
        ),
    ]
