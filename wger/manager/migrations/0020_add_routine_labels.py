# Generated by Django 4.2.13 on 2024-05-31 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('manager', '0019_flexible_routines_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayng',
            name='routine',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='days',
                to='manager.routine',
                verbose_name='Routine',
            ),
        ),
        migrations.AlterField(
            model_name='routine',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='day',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='slots',
                to='manager.dayng',
                verbose_name='Exercise day',
            ),
        ),
        migrations.AlterField(
            model_name='slotconfig',
            name='slot',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='configs',
                to='manager.slot',
            ),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'start_offset',
                    models.PositiveIntegerField(default=1, verbose_name='Start'),
                ),
                (
                    'end_offset',
                    models.PositiveIntegerField(default=2, verbose_name='End'),
                ),
                ('label', models.CharField(max_length=35, verbose_name='Label')),
                ('comment', models.CharField(max_length=500, verbose_name='Comment')),
                (
                    'routine',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='manager.routine',
                        verbose_name='Routine',
                    ),
                ),
            ],
        ),
    ]
