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
from typing import Optional

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox, QWidget

from mpvqc.gui.messageboxes.impls.mb_messagebox import MessageBox

_translate = QCoreApplication.translate


class UnsavedChangesQuitResponse(Enum):
    CANCEL = auto()
    QUIT = auto()


class UnsavedChangesQuitMessageBox(MessageBox):
    _RESPONSES = {
        QMessageBox.Yes: UnsavedChangesQuitResponse.QUIT,
        QMessageBox.No: UnsavedChangesQuitResponse.CANCEL,
    }

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._response = UnsavedChangesQuitResponse.CANCEL

    def popup(self) -> None:
        mb = QMessageBox(self._parent)
        mb.setWindowTitle(_translate("MessageBoxes", "Unsaved Changes"))
        mb.setText(_translate("MessageBoxes", "Do you really want to quit without saving your QC?"))
        mb.setIcon(QMessageBox.Critical)
        mb.addButton(QMessageBox.Yes)
        mb.addButton(QMessageBox.No)

        self._response = self._parse_response(from_mb=mb)

    def _parse_response(self, from_mb: QMessageBox) -> UnsavedChangesQuitResponse:
        response = from_mb.exec_()
        return self._RESPONSES.get(response)

    def response(self):
        return self._response
