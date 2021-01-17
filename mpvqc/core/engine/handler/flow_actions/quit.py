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


from mpvqc.core.engine.handler import FlowQuestion
from mpvqc.core.engine.handler.interactions import QuitUnsavedMessageBox
from mpvqc.core.engine.handler.layer import Response
from mpvqc.core.engine.interface import Options


class QuitFlowQuestion(FlowQuestion):

    def __init__(self, options: Options, have_unsaved_changes: bool):
        self._have_unsaved_changes = have_unsaved_changes
        self._response = not have_unsaved_changes

        self._mb_quit = QuitUnsavedMessageBox(options.app)

    def have_unsaved_changes(self) -> bool:
        return self._have_unsaved_changes

    def ask_via_message_box_to_quit(self):
        self._response = self._mb_quit.do_we_quit()

    def get_the_response(self) -> Response:
        return self._response
