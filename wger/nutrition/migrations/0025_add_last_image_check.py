# Generated by Django 4.2.16 on 2025-02-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('nutrition', '0024_remove_ingredient_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='last_image_check',
            field=models.DateTimeField(
                blank=True,
                default=None,
                null=True,
                editable=False,
            ),
        ),
    ]
