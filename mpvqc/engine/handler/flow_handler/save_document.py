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
from mpvqc.engine.handler.flow_actions import SaveDocumentFlowActions
from mpvqc.engine.interface import Options
from mpvqc.engine.states import SaveChanges


class SaveDocumentFlowHandler(FlowHandler):

    def __init__(self, current_file: Optional[Path]):
        self._current_file = current_file

        self._changes = SaveChanges()

    def handle_flow_with(self, options: Options) -> None:
        we = SaveDocumentFlowActions(options, self._current_file)

        if we.dont_have_write_path():
            we.ask_user_via_dialog_for_write_path()

        if we.have_write_path():
            try:
                we.write_document()
            except Exception:
                we.show_error()

        self._changes = we.get_changes()

    def get_changes(self) -> SaveChanges:
        return self._changes
