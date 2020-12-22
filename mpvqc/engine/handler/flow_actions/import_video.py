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

from mpvqc.engine.handler import FlowActions
from mpvqc.engine.handler.actions import VideoImporter
from mpvqc.engine.handler.interactions import VideoImportDialog, VideoFoundMessageBox
from mpvqc.engine.interface import Options
from mpvqc.engine.states import ImportChanges


class VideoImportFlowActions(FlowActions):

    def __init__(self, options: Options, video_path: Optional[Path]):
        self._player = options.player
        self._video_path = video_path

        self._dialog_video_import = VideoImportDialog(options.app)
        self._mb_open_found_video = VideoFoundMessageBox(options.app)

        self._action_video_import = VideoImporter(options.player)

        self._we_changed = ImportChanges()

    def dont_have_a_video(self) -> bool:
        return not self.have_video()

    def have_video(self) -> bool:
        return bool(self._video_path)

    def ask_via_dialog_for_video(self) -> None:
        self._video_path = self._dialog_video_import.get_video()

    def confirm_the_video_exists(self) -> bool:
        return self.have_video() and self._video_path.is_file()

    def see_the_video_is_not_already_playing(self) -> bool:
        return not self._video_is_currently_playing()

    def _video_is_currently_playing(self) -> bool:
        if self.have_video() and self._have_a_video_playing_already():
            playing = self._player.get_video()
            imported = self._video_path
            return playing.resolve() == imported.resolve()
        return False

    def _have_a_video_playing_already(self) -> bool:
        return bool(self._player.has_video())

    def ask_via_message_box_to_open_found_video(self) -> None:
        self._mb_open_found_video.ask()

    def want_to_open_found_video(self) -> bool:
        return self._mb_open_found_video.do_we_open()

    def load_video(self) -> None:
        self._action_video_import.load(self._video_path)
        self._we_changed.loaded_video = self._video_path

    def get_changes(self) -> ImportChanges:
        return self._we_changed
