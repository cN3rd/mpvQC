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
from typing import Optional, Tuple, List

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFileDialog

from mpvqc.gui.dialogs.impls.dialog import Dialog

_translate = QtCore.QCoreApplication.translate


class OpenDocumentsDialog(Dialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._documents: Tuple[Path] = tuple()

    def open(self, last_directory: Optional[Path]) -> None:
        documents = self._open_dialog(in_directory=last_directory)

        if documents:
            self._documents = self.as_paths(documents)

    def _open_dialog(self, in_directory: Optional[Path]) -> List[str]:
        caption = _translate("FileInteractionDialogs", "Open QC Document(s)")

        allowed = f"{_translate('FileInteractionDialogs', 'QC documents')} (*.txt);;" \
                  f"{_translate('FileInteractionDialogs', 'All files')} (*.*)"

        directory = str(in_directory) if in_directory else self.home_directory

        return QFileDialog.getOpenFileNames(self._parent, caption, directory, filter=allowed)[0]

    def get_documents(self) -> Tuple[Path]:
        return self._documents
