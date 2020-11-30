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
from PyQt5.QtWidgets import QFileDialog, QWidget

from mpvqc.gui.dialogs.dialog import Dialog
from mpvqc.gui.dialogs.save_path_suggester import SavePathSuggester

_translate = QtCore.QCoreApplication.translate


class SaveDialog(Dialog):

    PATH_SUGGESTER = SavePathSuggester()

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self._path: Optional[Path] = None

    def open(self, for_video: Optional[Path], and_nickname: Optional[str]) -> None:
        filepath = self._open_dialog(for_video, and_nickname)

        if filepath:
            self._path = Path(filepath)

    def _open_dialog(self, for_video: Optional[Path], and_writer: Optional[str]) -> str:
        caption = _translate("FileInteractionDialogs", "Save QC Document As")

        allowed = f"{_translate('FileInteractionDialogs', 'QC documents')} (*.txt);;" \
                  f"{_translate('FileInteractionDialogs', 'All files')} (*.*)"

        path = self.PATH_SUGGESTER.suggest(for_video, and_writer)

        return QFileDialog.getSaveFileName(self._parent, caption, str(path), filter=allowed)[0]

    def get_location(self) -> Optional[Path]:
        return self._path
