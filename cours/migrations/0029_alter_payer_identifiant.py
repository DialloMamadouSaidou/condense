# Generated by Django 4.2.5 on 2024-04-09 04:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cours", "0028_rename_module_payer_modules_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payer",
            name="identifiant",
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
