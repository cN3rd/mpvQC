# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path
from typing import Tuple

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

_translate = QCoreApplication.translate


class InvalidDocumentDuringImportMessageBox:

    def __init__(self, invalid_files: Tuple[Path]):
        self._invalid_files = invalid_files
        self._amount = len(invalid_files)

    def popup(self) -> None:
        mb = QMessageBox()
        mb.setWindowTitle(self._title())
        mb.setText(self._text())
        mb.setInformativeText(self._informative_text())
        mb.setIcon(QMessageBox.Information)
        mb.exec_()

    def _title(self) -> str:
        if self._amount == 1:
            return _translate("MessageBoxes", "Imported Document Not Compatible")
        return _translate("MessageBoxes", "Imported Documents Not Compatible")

    def _text(self) -> str:
        if self._amount == 1:
            return _translate("MessageBoxes", "The following file is not compatible:")
        return _translate("MessageBoxes", "The following files are not compatible:")

    def _informative_text(self) -> str:
        paths = map(lambda p: str(p), self._invalid_files)
        return '- {0}'.format(("\n- ".join(paths)))
