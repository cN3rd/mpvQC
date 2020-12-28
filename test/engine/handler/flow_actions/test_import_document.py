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


import unittest
from unittest.mock import patch, Mock

from mpvqc.doc_io import DocumentImport, Document, Incompatible
from mpvqc.engine.handler.flow_actions import DocumentImportFlowActions
from mpvqc.engine.interface import Options
from test.doc_io.input import ANY_PATH, ANY_PATHS, ANY_VIDEO
from test.engine import PlayerTestImpl, AppTestImpl, TableTestImpl


IMPORT_EMPTY = DocumentImport(documents=tuple(), incompatibles=tuple())

IMPORT_ONE_COMPATIBLE = DocumentImport(
    documents=tuple([Document(file=ANY_PATH, video=ANY_VIDEO, comments=tuple())]),
    incompatibles=tuple()
)

IMPORT_ONE_INCOMPATIBLE = DocumentImport(
    documents=tuple(),
    incompatibles=tuple([Incompatible(file=ANY_PATH)])
)

IMPORT_ONE_COMPATIBLE_NO_VIDEO = DocumentImport(
    documents=tuple([Document(file=ANY_PATH, video=None, comments=tuple())]),
    incompatibles=tuple()
)


class TestDocumentImportFlowActions(unittest.TestCase):
    GET_DOCUMENTS = 'mpvqc.engine.handler.flow_actions.import_document.DocumentImportDialog.get_documents'

    IMPORTER_IMPORT_THEM = 'mpvqc.engine.handler.flow_actions.import_document.Importer.import_them'
    IMPORTER_GET_IMPORT = 'mpvqc.engine.handler.flow_actions.import_document.Importer.get_import'

    MB_EXISTING_COMMENTS_ASK = 'mpvqc.engine.handler.flow_actions.import_document.ExistingCommentsMessageBox.ask'
    MB_EXISTING_COMMENTS_ABORT \
        = 'mpvqc.engine.handler.flow_actions.import_document.ExistingCommentsMessageBox.do_we_abort'
    MB_EXISTING_COMMENTS_CLEAR \
        = 'mpvqc.engine.handler.flow_actions.import_document.ExistingCommentsMessageBox.do_we_clear_table'

    TABLE_CLEARER_CLEAR = 'mpvqc.engine.handler.flow_actions.import_document.TableClearer.clear_table'

    COMMENTS_IMPORTER_LOAD = 'mpvqc.engine.handler.flow_actions.import_document.CommentsImporter.load'

    INCOMPATIBLES_SHOW = 'mpvqc.engine.handler.flow_actions.import_document.IncompatibleDocumentsMessageBox.show'

    OPTIONS = Options(
        AppTestImpl(),
        PlayerTestImpl(),
        TableTestImpl()
    )

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE)
    def test_video_from_document_existing(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.get_the_found_videos())
        we.import_paths()
        self.assertTrue(we.get_the_found_videos())

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE_NO_VIDEO)
    def test_video_from_document_not_existing(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.get_the_found_videos())
        we.import_paths()
        self.assertFalse(we.get_the_found_videos())

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE)
    def test_paths_from_imported_documents(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.get_all_paths_from_imported_documents())
        we.import_paths()
        self.assertTrue(we.get_all_paths_from_imported_documents())

    def test_have_paths(self):
        we = DocumentImportFlowActions(self.OPTIONS, tuple())

        self.assertFalse(we.have_any_paths())
        self.assertTrue(we.dont_have_any_paths())

    @patch(GET_DOCUMENTS, return_value=ANY_PATHS)
    def test_ask_via_dialog_for_paths(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, tuple())
        we.ask_via_dialog_for_paths()
        self.assertTrue(we.have_any_paths())

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE)
    def test_import_paths_ensure_documents_imported(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.have_documents_imported())
        we.import_paths()
        self.assertTrue(we.have_documents_imported())

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE)
    def test_import_paths_changes_registered_video_with_video(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertIsNone(we.get_changes().stored_video)
        we.import_paths()
        self.assertIsNotNone(we.get_changes().stored_video)

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE_NO_VIDEO)
    def test_import_paths_changes_registered_video_without_video(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertIsNone(we.get_changes().stored_video)
        we.import_paths()
        self.assertIsNone(we.get_changes().stored_video)

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_EMPTY)
    def test_import_paths_changes_registered_video_empty(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertIsNone(we.get_changes().stored_video)
        we.import_paths()
        self.assertIsNone(we.get_changes().stored_video)

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE)
    def test_import_paths_changes_registered_document_compatible(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.get_changes().loaded_documents)
        we.import_paths()
        self.assertTrue(we.get_changes().loaded_documents)

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_EMPTY)
    def test_import_paths_changes_registered_document_empty(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.get_changes().loaded_documents)
        we.import_paths()
        self.assertFalse(we.get_changes().loaded_documents)

    def test_neither_documents_nor_incompatibles_empty(self):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertTrue(we.neither_have_documents_nor_incompatibles_imported())

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE)
    def test_neither_documents_nor_incompatibles_compatibles(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        we.import_paths()
        self.assertFalse(we.neither_have_documents_nor_incompatibles_imported())

    def test_have_documents_imported_empty(self):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.have_documents_imported())

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_COMPATIBLE)
    def test_have_documents_imported_compatibles(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        we.import_paths()
        self.assertTrue(we.have_documents_imported())

    def test_have_comments(self):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.have_comments())

    @patch(MB_EXISTING_COMMENTS_ASK)
    def test_ask_via_message_box_what_to_do_with_comments(self, mocked_ask: Mock):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        we.ask_via_message_box_what_to_do_with_comments()
        mocked_ask.assert_called()

    @patch(MB_EXISTING_COMMENTS_ABORT)
    def test_want_to_abort_the_import(self, mocked_abort: Mock):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        we.want_to_abort_the_import()
        mocked_abort.assert_called()

    @patch(MB_EXISTING_COMMENTS_CLEAR)
    def test_want_to_clear_all_comments(self, mocked_clear: Mock):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        we.want_to_clear_all_comments()
        mocked_clear.assert_called()

    @patch(TABLE_CLEARER_CLEAR)
    def test_clear_all_comments_called(self, mocked_clear_table: Mock):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        we.clear_all_comments()
        mocked_clear_table.assert_called()

    @patch(TABLE_CLEARER_CLEAR)
    def test_clear_all_comments_changes_registered(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.get_changes().cleared_the_table)
        we.clear_all_comments()
        self.assertTrue(we.get_changes().cleared_the_table)

    @patch(COMMENTS_IMPORTER_LOAD)
    def test_load_comments(self, mocked_load: Mock):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        we.load_comments()
        mocked_load.assert_called()

    @patch(IMPORTER_IMPORT_THEM)
    @patch(IMPORTER_GET_IMPORT, return_value=IMPORT_ONE_INCOMPATIBLE)
    def test_have_incompatibles_imported(self, *_):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        self.assertFalse(we.have_incompatibles_imported())
        we.import_paths()
        self.assertTrue(we.have_incompatibles_imported())

    @patch(INCOMPATIBLES_SHOW)
    def test_show_via_message_box_all_incompatible_documents(self, mocked_show: Mock):
        we = DocumentImportFlowActions(self.OPTIONS, ANY_PATHS)
        we.show_via_message_box_all_incompatible_documents()
        mocked_show.assert_called()
