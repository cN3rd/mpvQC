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


from pathlib import Path
from typing import Iterator


from mpvqc.engine.interface import App
from mpvqc.gui.messageboxes import MessageBoxes


class IncompatibleDocumentsMessageBox:

    def __init__(self, app: App):
        self._parent = app.parent()
        self._incompatibles = tuple()

    def set_incompatibles(self, incompatibles: Iterator[Path]):
        self._incompatibles = tuple(incompatibles)

    def show(self) -> None:
        MessageBoxes.invalid_documents_during_import(self._incompatibles, self._parent)