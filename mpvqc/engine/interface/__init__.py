#  mpvQC
#
#  Copyright (C) 2020 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import NamedTuple

from mpvqc.engine.interface.app import App
from mpvqc.engine.interface.app_impl import AppImpl
from mpvqc.engine.interface.player import Player
from mpvqc.engine.interface.player_impl import PlayerImpl
from mpvqc.engine.interface.table import Table
from mpvqc.engine.interface.table_impl import TableImpl


class Options(NamedTuple):
    app: App
    player: Player
    table: Table
