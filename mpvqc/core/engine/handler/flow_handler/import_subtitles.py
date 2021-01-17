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

from mpvqc.core.engine.handler import FlowHandler
from mpvqc.core.engine.handler.flow_actions import SubtitleImportFlowActions
from mpvqc.core.engine.interface import Options
from mpvqc.core.engine.states import ImportChanges


class SubtitleImportFlowHandler(FlowHandler):

    def __init__(self, subtitle_paths: Tuple[Path] = tuple()):
        self._subtitle_paths = subtitle_paths

    def has_subtitle_paths(self) -> bool:
        return bool(self._subtitle_paths)

    def handle_flow_with(self, options: Options) -> None:
        we = SubtitleImportFlowActions(options, self._subtitle_paths)

        if we.dont_have_subtitles():
            we.ask_via_dialog_for_subtitles()

        if we.have_subtitles():
            we.load_subtitles()

    def get_changes(self):
        return ImportChanges()
