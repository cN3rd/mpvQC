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
from typing import Optional, Tuple

from mpvqc.core.engine.interface.player import Player
from mpvqc.core.player import MpvPlayer


class PlayerImpl(Player):

    def __init__(self, player: MpvPlayer):
        self._player = player

    def has_video(self) -> bool:
        return self._player.has_video()

    def get_video(self) -> Optional[Path]:
        if self.has_video():
            return Path(self._player.video_file_current())
        return None

    def open(self, video: Optional[Path] = None, subtitles: Optional[Tuple[Path]] = None) -> None:
        if video:
            self._player.open_video(video)
        if subtitles:
            for subtitle in subtitles:
                self._player.add_sub_files(subtitle)

    def pause(self) -> None:
        self._player.pause()
