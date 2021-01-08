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


from pathlib import Path
from typing import Optional

from PyQt5 import QtCore

_translate = QtCore.QCoreApplication.translate


class SavePathSuggester:

    @staticmethod
    def suggest(for_video: Optional[Path], and_writer: Optional[str]) -> Path:
        folder = SavePathSuggester._suggest_directory(for_video)
        filename = SavePathSuggester._suggest_filename(for_video, and_writer)
        return folder / filename

    @staticmethod
    def _suggest_directory(video: Optional[Path]) -> Path:
        return video.parent if video else Path.home()

    @staticmethod
    def _suggest_filename(video: Optional[Path], writer: Optional[str]) -> str:
        video = video.stem if video else _translate("FileInteractionDialogs", "untitled")
        writer = f'_{writer}' if writer else ''
        return f'[QC]_{video}{writer}.txt'
