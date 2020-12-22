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

from mpvqc.engine.handler import FlowHandler
from mpvqc.engine.handler.flow_actions import VideoImportFlowActions
from mpvqc.engine.interface import Options
from mpvqc.engine.states import ImportChanges


class VideoImportFlowHandler(FlowHandler):

    def __init__(self, video: Optional[Path] = None):
        self._video = video
        self._changes = ImportChanges()

    def has_video_path(self) -> bool:
        return bool(self._video)

    def handle_flow_with(self, options: Options) -> None:
        we = VideoImportFlowActions(options, self._video)

        if we.dont_have_a_video():
            we.ask_via_dialog_for_video()

        if we.have_video():

            if we.see_the_video_is_not_already_playing():
                we.load_video()

        self._changes = self._changes.combine_with(we.get_changes())

    def get_changes(self) -> ImportChanges:
        return self._changes

