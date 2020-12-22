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


from mpvqc.engine.states.changes_comments import CommentsChanges
from mpvqc.engine.states.changes_import import ImportChanges
from mpvqc.engine.states.changes_new import NewDocumentChanges
from mpvqc.engine.states.changes_save import SaveChanges
from mpvqc.engine.states.state import State


def initial_state() -> State:
    from mpvqc.engine.states.state import InitialState
    return InitialState(video=None, stored_video=None)
