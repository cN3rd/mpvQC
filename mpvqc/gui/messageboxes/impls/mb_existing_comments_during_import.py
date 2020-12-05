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


class ExistingCommentsDuringImportResponse(Enum):
    CANCEL_IMPORT = auto()
    DELETE_COMMENTS = auto()
    KEEP_COMMENTS = auto()


class ExistingCommentsDuringImportMessageBox:
    _RESPONSES = {
        0: ExistingCommentsDuringImportResponse.DELETE_COMMENTS,
        1: ExistingCommentsDuringImportResponse.KEEP_COMMENTS,
        QMessageBox.Abort: ExistingCommentsDuringImportResponse.CANCEL_IMPORT,
    }

    def __init__(self):
        self._response = ExistingCommentsDuringImportResponse.CANCEL_IMPORT

    def popup(self) -> None:
        mb = QMessageBox()
        mb.setWindowTitle(_translate("MessageBoxes", "Existing Comments"))
        mb.setText(_translate("MessageBoxes", "What do you want to do with the existing comments?"))
        mb.setIcon(QMessageBox.Question)
        mb.addButton(QMessageBox.Abort)
        mb.addButton(_translate("MessageBoxes", "Delete"), QMessageBox.YesRole)
        mb.addButton(_translate("MessageBoxes", "Keep"), QMessageBox.NoRole)

        self._response = self._parse_response(from_mb=mb)

    def _parse_response(self, from_mb: QMessageBox) -> ExistingCommentsDuringImportResponse:
        response = from_mb.exec_()
        return self._RESPONSES.get(response)

    def response(self):
        return self._response
