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


from mpvqc.core.engine.handler import UserQuestionHandler
from mpvqc.core.engine.handler.flow_actions import QuitFlowQuestion
from mpvqc.core.engine.handler.layer import Response
from mpvqc.core.engine.interface import Options


class QuitQuestionFlowHandler(UserQuestionHandler):

    def __init__(self, have_unsaved_changes: bool):
        self._have_unsaved_changes = have_unsaved_changes

    def ask_with(self, options: Options) -> Response:
        we = QuitFlowQuestion(options, have_unsaved_changes=self._have_unsaved_changes)

        if we.have_unsaved_changes():
            we.ask_via_message_box_to_quit()

        return we.get_the_response()
