# Generated by Django 4.2.5 on 2024-02-19 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0011_alter_chapitre_module"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="chapitre",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cours.chapitre",
            ),
        ),
    ]
