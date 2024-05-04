# Generated by Django 4.2.5 on 2024-05-03 23:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0035_planification"),
    ]

    operations = [
        migrations.AddField(
            model_name="planification",
            name="ponderation",
            field=models.CharField(
                default=django.utils.timezone.now,
                max_length=255,
                verbose_name="ponderation",
            ),
            preserve_default=False,
        ),
    ]