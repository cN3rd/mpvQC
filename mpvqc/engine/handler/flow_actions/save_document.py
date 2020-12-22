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

from mpvqc.doc_io import Document
from mpvqc.engine.handler import FlowActions
from mpvqc.engine.handler.actions import DocumentExporter
from mpvqc.engine.handler.interactions import SaveDialog, SaveErrorMessageBox
from mpvqc.engine.interface import Options
from mpvqc.engine.states import SaveChanges


class SaveDocumentFlowActions(FlowActions):

    def __init__(self, options: Options, current_file: Optional[Path]):
        self._current_file = current_file
        self._current_video = options.player.get_video()
        self._current_comments = options.table.get_all_comments()

        self._dialog_save = SaveDialog(options.app)
        self._dialog_save.set_video(self._current_video)
        self._mb_save_error = SaveErrorMessageBox(options.app)

        self._we_changed = SaveChanges()

    def dont_have_write_path(self) -> bool:
        return not self.have_write_path()

    def have_write_path(self) -> bool:
        return bool(self._current_file)

    def ask_user_via_dialog_for_write_path(self) -> None:
        self._current_file = self._dialog_save.get_write_path()

    def write_document(self) -> None:
        document = Document(
            file=self._current_file,
            video=self._current_video,
            comments=self._current_comments
        )
        DocumentExporter.export(document)
        self._we_changed.save_path = self._current_file

    def show_error(self) -> None:
        self._mb_save_error.show()

    def get_changes(self) -> SaveChanges:
        return self._we_changed
