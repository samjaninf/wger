# Generated by Django 3.1.3 on 2020-12-01 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0006_auto_20201201_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercisevariation',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
    ]