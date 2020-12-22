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


from mpvqc.engine.handler import FlowActions
from mpvqc.engine.handler.actions import TableClearer
from mpvqc.engine.handler.interactions import NewDocumentMessageBox
from mpvqc.engine.interface import Options
from mpvqc.engine.states import NewDocumentChanges


class NewDocumentFlowActions(FlowActions):

    def __init__(self, options: Options, have_unsaved_changes: bool):
        self._table = options.table
        self._have_unsaved_changes = have_unsaved_changes

        self._mb_new_document = NewDocumentMessageBox(options.app)
        self._action_clear_table = TableClearer(options.table)

        self._we_changed = NewDocumentChanges()

    def have_unsaved_changes(self) -> bool:
        return self._have_unsaved_changes

    def ask_via_message_box_to_create_new_document(self) -> None:
        self._mb_new_document.ask()

    def want_to_create_new_document(self) -> bool:
        return self._mb_new_document.do_we_create_new()

    def clear_comments(self) -> None:
        self._action_clear_table.clear_table()
        self._we_changed.cleared_the_table = True

    def get_changes(self) -> NewDocumentChanges:
        return self._we_changed
