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


from mpvqc.engine.states.state import State, InitialState


class NewDocumentChanges:

    def __init__(self):
        self.cleared_the_table: bool = False


class NewDocumentEvaluator:

    def __init__(self, changes: NewDocumentChanges, state: State):
        self._we = changes
        self._current = state

    def evaluate(self) -> State:
        we, current = self._we, self._current

        if we.cleared_the_table:
            return InitialState(
                video=current.video,
                stored_video=current.stored_video if not current.video else None
            )

        return self._current
