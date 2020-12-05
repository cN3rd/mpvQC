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
from PyQt5.QtWidgets import QWidget, QFileDialog

from mpvqc.gui.filedialogs.impls.fd_dialog import Dialog

_translate = QtCore.QCoreApplication.translate


class OpenVideoDialog(Dialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._video: Optional[Path] = None

    def open(self, last_directory: Optional[Path]) -> None:
        video = self._open_dialog(in_directory=last_directory)

        if video:
            self._video = Path(video[0])

    def _open_dialog(self, in_directory: Optional[Path]) -> str:
        caption = _translate("FileInteractionDialogs", "Open Video File")

        directory = str(in_directory) if in_directory else self.home_directory

        allowed = f"{_translate('FileInteractionDialogs', 'Video files')} (*.mp4 *.mkv *.avi);;" \
                  f"{_translate('FileInteractionDialogs', 'All files')} (*.*)"

        return QFileDialog.getOpenFileName(self._parent, caption, directory, filter=allowed)[0]

    def get_video(self) -> Optional[Path]:
        return self._video


