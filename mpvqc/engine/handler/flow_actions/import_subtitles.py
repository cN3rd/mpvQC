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
from typing import Tuple

from mpvqc.engine.handler.actions import SubtitleImporter
from mpvqc.engine.handler.interactions import SubtitleImportDialog
from mpvqc.engine.interface import Options


class SubtitleImportFlowActions:

    def __init__(self, options: Options, subtitle_paths: Tuple[Path]):
        self._options = options

        self._subtitle_paths = subtitle_paths

        self._dialog_subtitle_import = SubtitleImportDialog(options.app)
        self._importer_subtitles = SubtitleImporter(options.player)

    def dont_have_subtitles(self) -> bool:
        return not self.have_subtitles()

    def have_subtitles(self) -> bool:
        return bool(self._subtitle_paths)

    def ask_via_dialog_for_subtitles(self) -> None:
        self._subtitle_paths = self._dialog_subtitle_import.get_subtitles()

    def load_subtitles(self) -> None:
        self._importer_subtitles.load(self._subtitle_paths)
