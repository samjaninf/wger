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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

# Third Party
from django_filters import (
    UnknownFieldBehavior,
    rest_framework as filters,
)

# wger
from wger.manager.api.consts import BASE_CONFIG_FILTER_FIELDS


class BaseConfigFilterSet(filters.FilterSet):
    class Meta:
        fields = BASE_CONFIG_FILTER_FIELDS
        unknown_field_behavior = UnknownFieldBehavior.IGNORE
