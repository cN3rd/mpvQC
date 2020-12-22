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


from PyQt5.QtCore import QTimer

from mpvqc import get_settings
from mpvqc.doc_io import Document
from mpvqc.engine.handler.actions import DocumentExporter
from mpvqc.engine.interface import Options


class Backup:

    def __init__(self, options: Options):
        self._options = options
        self._timer = QTimer()

        self._table = options.table
        self._player = options.player

        self._continue_until_stopped_manually = True

    def reset_timer(self):
        self._timer.stop()

        s = get_settings()
        interval = s.backup_interval

        if interval and interval >= 15:
            self._timer = QTimer()
            self._timer.timeout.connect(self._backup)
            self._timer.start(interval * 1000)

    def _backup(self) -> bool:
        document = Document(file=None, video=self._player.get_video(), comments=self._table.get_all_comments())
        DocumentExporter.backup(document)
        return self._continue_until_stopped_manually
