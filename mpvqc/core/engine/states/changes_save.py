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

from mpvqc.core import Comment
from mpvqc.core.engine.states.state import State, SavedState


class SaveChanges:

    def __init__(self):
        self.save_path: Optional[Path] = None


class SaveEvaluator:

    def __init__(self, changes: SaveChanges, state: State, comments: Tuple[Comment]):
        self._changes = changes
        self._current = state
        self._comments = comments

    def evaluate(self) -> State:
        new, current, comments = self._changes, self._current, self._comments

        save_path = new.save_path or current.path

        if save_path:
            return SavedState(
                file=save_path,
                video=current.video,
                stored_video=None,
                comments=comments
            )

        return current
