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
from typing import Optional

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QInputDialog

from .fd_dialog import Dialog

_translate = QtCore.QCoreApplication.translate


class OpenNetworkStreamDialog(Dialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._path: Optional[str] = None

    def open(self) -> None:
        dialog = QInputDialog(self._parent)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle(_translate("FileInteractionDialogs", "Open Network Stream"))
        dialog.setLabelText(_translate("FileInteractionDialogs", "Enter URL:"))
        dialog.resize(700, 0)
        dialog.exec_()

        path = dialog.textValue()
        if path:
            self._path = Path(path)

    def get_path(self) -> Optional[Path]:
        return self._path
