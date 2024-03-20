# Generated by Django 4.2.5 on 2024-03-19 20:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0009_rename_paie_profile_pai"),
        ("cours", "0023_alter_choix_cours_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="note",
            options={
                "ordering": ["note"],
                "verbose_name": "note",
                "verbose_name_plural": "Note Etudiant",
            },
        ),
        migrations.AlterField(
            model_name="note",
            name="commentaire",
            field=models.CharField(default="", max_length=500),
        ),
        migrations.AlterField(
            model_name="note",
            name="note",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(20),
                ]
            ),
        ),
        migrations.AlterUniqueTogether(
            name="note",
            unique_together={("module", "etudiant")},
        ),
    ]