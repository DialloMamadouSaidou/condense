# Generated by Django 4.2.5 on 2024-06-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0056_remove_create_groupe_document_file_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="create_groupe",
            name="examen_concerne",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name="create_groupe",
            name="note",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]