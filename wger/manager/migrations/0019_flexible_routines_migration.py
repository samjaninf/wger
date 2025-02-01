# Generated by Django 4.2.6 on 2024-04-14 11:22
from typing import Any

from django.db import migrations

from datetime import timedelta


def migrate_forward(apps, schema_editor):
    workouts_to_routines = migrate_routines(apps)
    migrate_sessions(apps, workouts_to_routines)
    migrate_logs(apps, workouts_to_routines)


def migrate_routines(apps) -> dict[int, Any]:
    """
    Migrates all workouts to routines and the new data model
    """

    Workout = apps.get_model('manager', 'Workout')
    Routine = apps.get_model('manager', 'Routine')
    DayNg = apps.get_model('manager', 'DayNg')
    Slot = apps.get_model('manager', 'Slot')
    SlotEntry = apps.get_model('manager', 'SlotEntry')
    SetsConfig = apps.get_model('manager', 'SetsConfig')
    WeightConfig = apps.get_model('manager', 'WeightConfig')
    RepetitionsConfig = apps.get_model('manager', 'RepetitionsConfig')
    RiRConfig = apps.get_model('manager', 'RiRConfig')
    RestConfig = apps.get_model('manager', 'RestConfig')

    REPLACE_OP = 'r'
    ABS_STEP = 'abs'

    workouts_to_routines = {}

    for workout in Workout.objects.all():
        next_monday = workout.creation_date + timedelta(days=7 - workout.creation_date.weekday())

        routine = Routine(
            name=workout.name[:25],
            description=workout.description,
            user=workout.user,
            created=workout.creation_date,
            start=next_monday,
            end=next_monday + timedelta(weeks=16),
            is_template=workout.is_template,
            is_public=workout.is_public,
            fit_in_week=False,
        )
        routine.save()

        workouts_to_routines[workout.id] = routine

        day_dict = {}

        # To simulate a hard coded week, we will create exactly seven day entries (since
        # we know the routine starts on a monday).
        for i in range(1, 8):
            current_day = DayNg(routine=routine, order=i, is_rest=True)
            current_day.save()
            day_dict[i] = current_day

        for i in range(1, 8):
            current_day = day_dict[i]

            day = workout.day_set.filter(day__id=i).first()
            if day:
                current_day.name = day.description[:20]
                current_day.description = day.description
                current_day.is_rest = False
                current_day.need_logs_to_advance = False
                current_day.save()

                # Set the exercises and repetitions
                for set_obj in day.set_set.all():
                    slot = Slot(day=current_day, comment=set_obj.comment, order=set_obj.order)
                    slot.save()
                    for setting in set_obj.setting_set.all():
                        slot_entry = SlotEntry(
                            slot=slot,
                            exercise=setting.exercise_base,
                            # default "reps"
                            repetition_unit_id=setting.repetition_unit_id
                            if setting.repetition_unit_id is not None
                            else 1,
                            # default "kg"
                            weight_unit_id=setting.weight_unit_id
                            if setting.weight_unit_id is not None
                            else 1,
                            order=setting.order,
                            comment=setting.comment,
                        )
                        slot_entry.save()

                        if setting.weight:
                            WeightConfig(
                                slot_entry=slot_entry,
                                value=setting.weight,
                                iteration=1,
                                operation=REPLACE_OP,
                                step=ABS_STEP,
                            ).save()

                        if setting.reps:
                            RepetitionsConfig(
                                slot_entry=slot_entry,
                                value=setting.reps,
                                iteration=1,
                                operation=REPLACE_OP,
                                step=ABS_STEP,
                            ).save()

                        if setting.rir:
                            RiRConfig(
                                slot_entry=slot_entry,
                                value=setting.rir,
                                iteration=1,
                                operation=REPLACE_OP,
                                step=ABS_STEP,
                            ).save()

                        RestConfig(
                            slot_entry=slot_entry,
                            value=120,
                            iteration=1,
                            operation=REPLACE_OP,
                            step=ABS_STEP,
                        ).save()

                        SetsConfig(
                            slot_entry=slot_entry,
                            value=set_obj.sets,
                            iteration=1,
                            operation=REPLACE_OP,
                            step=ABS_STEP,
                        ).save()

        routine.first_day = day_dict[1]
        routine.save()
    return workouts_to_routines


def migrate_sessions(apps, workout_to_routine: dict[int, Any]) -> None:
    Session = apps.get_model('manager', 'WorkoutSession')
    for session in Session.objects.all():
        if session.workout:
            session.routine = workout_to_routine[session.workout.id]
            session.save()


def migrate_logs(apps, workout_to_routine: dict[int, Any]) -> None:
    """
    Migrates all logs to the new data model (basically setting the routine and session)
    """

    Log = apps.get_model('manager', 'WorkoutLog')
    Session = apps.get_model('manager', 'WorkoutSession')

    for log in Log.objects.all():
        pass
        if not log.workout:
            continue

        session, created = Session.objects.get_or_create(
            user=log.user,
            date=log.date.date(),
            routine=workout_to_routine[log.workout.id],
            defaults={
                'workout': log.workout,
            },
        )
        log.routine = workout_to_routine[log.workout.id]
        log.session = session
        log.save()


class Migration(migrations.Migration):
    dependencies = [
        ('manager', '0018_flexible_routines'),
    ]

    operations = [
        migrations.RunPython(migrate_forward, reverse_code=migrations.RunPython.noop),
    ]
