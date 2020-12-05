# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path
from typing import Tuple

from mpvqc.gui.messageboxes.impls.mb_could_not_save_document import \
    CouldNotSaveDocumentMessageBox
from mpvqc.gui.messageboxes.impls.mb_existing_comments_during_import import \
    ExistingCommentsDuringImportMessageBox, \
    ExistingCommentsDuringImportResponse
from mpvqc.gui.messageboxes.impls.mb_invalid_document_during_import import \
    InvalidDocumentDuringImportMessageBox
from mpvqc.gui.messageboxes.impls.mb_unsaved_changes_create_new_document import \
    UnsavedChangesCreateNewDocumentResponse, \
    UnsavedChangesCreateNewDocumentMessageBox
from mpvqc.gui.messageboxes.impls.mb_unsaved_changes_quit import \
    UnsavedChangesQuitResponse, \
    UnsavedChangesQuitMessageBox
from mpvqc.gui.messageboxes.impls.mb_valid_video_file_found import \
    ValidVideoFileFoundResponse, \
    ValidVideoFileFoundMessageBox


class MessageBoxes:

    @staticmethod
    def could_not_save_document() -> None:
        mb = CouldNotSaveDocumentMessageBox()
        mb.popup()

    @staticmethod
    def existing_comments_during_import() -> ExistingCommentsDuringImportResponse:
        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()
        return mb.response()

    @staticmethod
    def invalid_documents_during_import(invalid_files: Tuple[Path]) -> None:
        mb = InvalidDocumentDuringImportMessageBox(invalid_files)
        mb.popup()

    @staticmethod
    def unsaved_changes_create_new_document() -> UnsavedChangesCreateNewDocumentResponse:
        mb = UnsavedChangesCreateNewDocumentMessageBox()
        mb.popup()
        return mb.response()

    @staticmethod
    def unsaved_changes_quit() -> UnsavedChangesQuitResponse:
        mb = UnsavedChangesQuitMessageBox()
        mb.popup()
        return mb.response()

    @staticmethod
    def valid_video_found() -> ValidVideoFileFoundResponse:
        mb = ValidVideoFileFoundMessageBox()
        mb.popup()
        return mb.response()
