# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path
from typing import Optional, List, Tuple

from PyQt5.QtWidgets import QWidget


class Dialog:

    def __init__(self, parent: Optional[QWidget]):
        self._parent = parent

    @property
    def home_directory(self):
        return str(Path.home())

    @staticmethod
    def as_paths(paths: List[str]) -> Tuple[Path]:
        # noinspection PyTypeChecker
        return tuple(Path(path) for path in paths)
