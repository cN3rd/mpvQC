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
from typing import Tuple, Optional

from mpvqc.core import Comment
from mpvqc.core.engine.interface import Table, Player, App, Options


class AppTestImpl(App):

    def __init__(self, parent: Optional[any] = None):
        self._parent = parent

        self.parent_called = False

    def parent(self):
        self.parent_called = True
        return self._parent


class PlayerTestImpl(Player):

    def __init__(self, has_video: bool = False, video: Optional[Path] = None):
        self._has_video = has_video
        self.video = video

        self._open_video_args = None
        self._open_subtitles_args = None

        self.has_video_called = False
        self.get_video_called = False
        self.open_called = False
        self.pause_called = False

    def has_video(self) -> bool:
        self.has_video_called = True
        return self._has_video

    def get_video(self) -> Optional[Path]:
        self.get_video_called = True
        return self.video

    def open(self, video: Optional[Path] = None, subtitles: Optional[Tuple[Path]] = None) -> None:
        self.open_called = True
        self.video = video
        self._open_video_args = video
        self._open_subtitles_args = subtitles

    def pause(self) -> None:
        self.pause_called = True


class TableTestImpl(Table):

    def __init__(self, has_comments: bool = False, comments: Tuple[Comment] = tuple()):
        self.has_comments_response = has_comments
        self.add_arguments = None

        self._comments = list(comments)

        self.has_comments_called = False
        self.add_called = False
        self.get_comments_called = False
        self.clear_comments_called = False

    def has_comments(self) -> bool:
        self.has_comments_called = True
        return self.has_comments_response

    def add(self, comments: Tuple[Comment]):
        self.add_called = True
        self.add_arguments = comments
        self._comments.extend(comments)

    def get_all_comments(self) -> Tuple[Comment]:
        self.get_comments_called = True
        return tuple(self._comments)

    def clear_comments(self) -> None:
        self.clear_comments_called = True
        self._comments.clear()


DEFAULT_OPTIONS = Options(
    AppTestImpl(),
    PlayerTestImpl(),
    TableTestImpl()
)
