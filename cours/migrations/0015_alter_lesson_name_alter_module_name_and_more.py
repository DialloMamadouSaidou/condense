# Generated by Django 4.2.5 on 2024-02-25 03:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0014_alter_chapitre_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="name",
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name="module",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="programme",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
