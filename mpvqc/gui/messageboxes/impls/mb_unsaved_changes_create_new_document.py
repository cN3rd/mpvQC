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


class UnsavedChangesCreateNewDocumentResponse(Enum):
    CANCEL = auto()
    CREATE_NEW = auto()


class UnsavedChangesCreateNewDocumentMessageBox:
    _RESPONSES = {
        QMessageBox.Yes: UnsavedChangesCreateNewDocumentResponse.CREATE_NEW,
        QMessageBox.No: UnsavedChangesCreateNewDocumentResponse.CANCEL,
    }

    def __init__(self):
        self._response = UnsavedChangesCreateNewDocumentResponse.CANCEL

    def popup(self) -> None:
        mb = QMessageBox()
        mb.setWindowTitle(_translate("MessageBoxes", "Unsaved Changes"))
        mb.setText(_translate("MessageBoxes", "Do you really want to create a new QC document without saving your QC?"))
        mb.setIcon(QMessageBox.Critical)
        mb.addButton(QMessageBox.Yes)
        mb.addButton(QMessageBox.No)

        self._response = self._parse_response(from_mb=mb)

    def _parse_response(self, from_mb: QMessageBox) -> UnsavedChangesCreateNewDocumentResponse:
        response = from_mb.exec_()
        get = self._RESPONSES.get(response)
        return get

    def response(self):
        return self._response
