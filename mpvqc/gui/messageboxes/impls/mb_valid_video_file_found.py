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


from enum import Enum, auto

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

_translate = QCoreApplication.translate


class ValidVideoFileFoundResponse(Enum):
    NOT_OPEN = auto()
    OPEN = auto()


class ValidVideoFileFoundMessageBox:
    _RESPONSES = {
        QMessageBox.Yes: ValidVideoFileFoundResponse.OPEN,
        QMessageBox.No: ValidVideoFileFoundResponse.NOT_OPEN,
    }

    def __init__(self):
        self._response = ValidVideoFileFoundResponse.NOT_OPEN

    def popup(self) -> None:
        mb = QMessageBox()
        mb.setWindowTitle(_translate("MessageBoxes", "Video Found"))
        mb.setText(_translate("MessageBoxes", "A video was found. Do you want to open it?"))
        mb.setIcon(QMessageBox.Question)
        mb.addButton(QMessageBox.Yes)
        mb.addButton(QMessageBox.No)

        self._response = self._parse_response(from_mb=mb)

    def _parse_response(self, from_mb: QMessageBox) -> ValidVideoFileFoundResponse:
        response = from_mb.exec_()
        return self._RESPONSES.get(response)

    def response(self):
        return self._response
