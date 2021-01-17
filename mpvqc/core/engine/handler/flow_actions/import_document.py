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
from typing import Tuple, Iterator

from mpvqc.core import Comment
from mpvqc.core.utility import flat_map
from mpvqc.doc_io import Importer, DocumentImport
from mpvqc.core.engine.handler import FlowActions
from mpvqc.core.engine.handler.actions import TableClearer, CommentsImporter
from mpvqc.core.engine.handler.interactions import DocumentImportDialog, ExistingCommentsMessageBox, \
    IncompatibleDocumentsMessageBox
from mpvqc.core.engine.interface import Options
from mpvqc.core.engine.states import ImportChanges


class DocumentImportFlowActions(FlowActions):

    def __init__(self, options: Options, document_paths: Tuple[Path]):
        self._table = options.table
        self._document_paths = document_paths

        self._import: DocumentImport = Importer.EMPTY_IMPORT
        self._document_paths_compatibles: Tuple[Path] = tuple()
        self._document_referenced_videos: Tuple[Path] = tuple()

        self._dialog_documents_import = DocumentImportDialog(options.app)
        self._mb_existing_comments = ExistingCommentsMessageBox(options.app)
        self._mb_show_incompatibles = IncompatibleDocumentsMessageBox(options.app)

        self._action_clear_table = TableClearer(options.table)
        self._action_comments_importer = CommentsImporter(options.table)

        self._we_changed = ImportChanges()

    def get_changes(self) -> ImportChanges:
        return self._we_changed

    def get_the_found_videos(self) -> Tuple[Path]:
        return self._document_referenced_videos

    def get_all_paths_from_imported_documents(self) -> Tuple[Path]:
        return self._document_paths_compatibles

    def dont_have_any_paths(self) -> bool:
        return not self.have_any_paths()

    def have_any_paths(self) -> bool:
        return bool(self._document_paths)

    def ask_via_dialog_for_paths(self) -> None:
        self._document_paths = self._dialog_documents_import.get_documents()

    def import_paths(self) -> None:
        importer = Importer(self._document_paths)
        importer.import_them()
        self._import = importer.get_import()
        self._after_paths_imported()

    def _after_paths_imported(self) -> None:
        self._store_video_found_in_documents()
        self._store_compatible_paths()

    def _store_video_found_in_documents(self) -> None:
        videos = tuple([doc.video for doc in self._import.documents if doc.video])
        self._document_referenced_videos = videos

        if videos:
            self._we_changed.stored_video = videos[0]

    def _store_compatible_paths(self) -> None:
        # noinspection PyTypeChecker
        paths: Tuple[Path] = tuple(map(lambda doc: doc.file, self._import.documents))
        self._document_paths_compatibles = paths
        self._we_changed.loaded_documents = paths

    def neither_have_documents_nor_incompatibles_imported(self) -> bool:
        return not bool(self._import.documents or self._import.incompatibles)

    def have_documents_imported(self) -> bool:
        return bool(self._import.documents)

    def have_comments(self) -> bool:
        return self._table.has_comments()

    def ask_via_message_box_what_to_do_with_comments(self) -> None:
        return self._mb_existing_comments.ask()

    def want_to_abort_the_import(self) -> bool:
        return self._mb_existing_comments.do_we_abort()

    def want_to_clear_all_comments(self) -> bool:
        return self._mb_existing_comments.do_we_clear_table()

    def clear_all_comments(self) -> None:
        self._action_clear_table.clear_table()
        self._we_changed.cleared_the_table = True

    def load_comments(self) -> None:
        comments: Tuple[Comment] = flat_map(lambda document: document.comments, self._import.documents)
        self._action_comments_importer.load(comments)

    def have_incompatibles_imported(self) -> bool:
        return bool(self._import.incompatibles)

    def show_via_message_box_all_incompatible_documents(self) -> None:
        incompatibles: Iterator[Path] = map(lambda incompatible: incompatible.file, self._import.incompatibles)
        self._mb_show_incompatibles.set_incompatibles(tuple(incompatibles))
        self._mb_show_incompatibles.show()
