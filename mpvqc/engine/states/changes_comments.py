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


from typing import Tuple

from mpvqc.core import Comment
from mpvqc.engine.states.state import State, UnsavedState


class CommentsChanges:

    def __init__(self):
        self.changed_comments: bool = False


class CommentsEvaluator:

    def __init__(self, changes: CommentsChanges, state: State, comments: Tuple[Comment]):
        self._we = changes
        self._current = state
        self._comments = comments

    def evaluate(self) -> State:
        current, comments = self._current, self._comments

        if self._we.changed_comments:
            return UnsavedState(
                file=current.path,
                video=current.video,
                stored_video=None,
                comments=comments
            )

        return current
