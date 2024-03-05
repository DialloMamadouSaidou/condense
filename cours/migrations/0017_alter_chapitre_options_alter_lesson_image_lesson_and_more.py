# Generated by Django 4.2.5 on 2024-02-29 23:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0016_alter_chapitre_unique_together"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chapitre",
            options={"ordering": ["module"]},
        ),
        migrations.AlterField(
            model_name="lesson",
            name="image_lesson",
            field=models.ImageField(blank=True, null=True, upload_to="image_crs/"),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="pdf_lesson",
            field=models.FileField(blank=True, null=True, upload_to="pdf_crs/"),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="video_lesson",
            field=models.FileField(blank=True, null=True, upload_to="video_crs/"),
        ),
    ]
