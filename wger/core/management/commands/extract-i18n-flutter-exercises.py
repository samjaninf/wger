# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

# Django
from django.core.management.base import BaseCommand

# wger
from wger.exercises.models import Translation


class Command(BaseCommand):
    help = (
        'Helper command to extract translations for the exercises used in the flutter repo for '
        'the screenshots for the play store'
    )

    uuids = {
        'squats': '30ac081b-fb79-4253-9457-8efc07568790',
        'benchPress': '3717d144-7815-4a97-9a56-956fb889c996',
        'deadLift': 'ee8e8db4-2d82-49e1-ab7f-891e9a354934',
        'crunches': 'b186f1f8-4957-44dc-bf30-d0b00064ce6f',
        'curls': '1ae6a28d-10e7-4ecf-af4f-905f8193e2c6',
        'raises': '63375f5b-2d81-471c-bea4-fc3d207e96cb',
    }

    def handle(self, **options):
        out = []
        languages = []

        for exercise_key in self.uuids.keys():
            self.stdout.write(f'Extracting translations for {exercise_key}')

            uuid = self.uuids[exercise_key]
            translations = Translation.objects.filter(exercise__uuid=uuid)

            variables = []

            for translation in translations:
                variable_name = f'{exercise_key}{translation.language.short_name.upper()}'
                variables.append(variable_name)

                if translation.language not in languages:
                    languages.append(translation.language)

                self.stdout.write(
                    f'- translation {translation.language.short_name}: {translation.name}'
                )

                out.append(
                    f"""
                    final {variable_name} = Translation(
                          id: {translation.id},
                          uuid: '{translation.uuid}',
                          created: DateTime(2021, 1, 15),
                          name: '{translation.name}',
                          description: '''{translation.description}''',
                          baseId: {translation.exercise_id},
                          language: tLanguage{translation.language.id},
                        );
                    """
                )
            self.stdout.write('')

            out.append(f'final {exercise_key}Translations = [{",".join(variables)}];')

        for language in languages:
            out.insert(
                0,
                f"""const tLanguage{language.id} =  Language(
                    id: {language.id},
                    shortName: '{language.short_name}',
                    fullName: '{language.full_name}',
                );""",
            )

        out.insert(0, "import 'package:wger/models/exercises/language.dart';")
        out.insert(0, "import 'package:wger/models/exercises/translation.dart';")
        out.insert(0, '// Autogenerated by extract-i18n-flutter-exercises.py do not edit!')

        #
        # Write to output
        with open('screenshots_exercises.dart', 'w') as f:
            f.write('\n'.join(out))
            self.stdout.write(self.style.SUCCESS('Wrote content to screenshots_exercises.dart'))
