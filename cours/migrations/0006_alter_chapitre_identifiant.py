# Generated by Django 4.2.5 on 2024-02-18 00:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0005_alter_module_options_module_programme"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chapitre",
            name="identifiant",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]