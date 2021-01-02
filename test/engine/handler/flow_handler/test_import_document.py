#  mpvQC
#
#  Copyright (C) 2021 mpvQC developers
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

from mpvqc.engine.handler.flow_handler import DocumentImportFlowHandler
from mpvqc.engine.interface import Options
from test.doc_io.input import ANY_PATHS, ANY_VIDEO, ANY_PATH
from test.engine import PlayerTestImpl, AppTestImpl, TableTestImpl


class Test(unittest.TestCase):
    DOC_FLOW_ACTIONS = 'mpvqc.engine.handler.flow_handler.import_document.DocumentImportFlowActions'
    VID_FLOW_ACTIONS = 'mpvqc.engine.handler.flow_handler.import_document.VideoImportFlowActions'

    OPTIONS = Options(
        AppTestImpl(),
        PlayerTestImpl(),
        TableTestImpl()
    )

    def test_unchanged(self):
        handler = DocumentImportFlowHandler()
        changes = handler.get_changes()
        self.assert_unchanged(changes)

    def assert_unchanged(self, changes):
        self.assertFalse(changes.cleared_the_table)
        self.assertFalse(changes.loaded_documents)
        self.assertFalse(changes.loaded_video)
        self.assertFalse(changes.stored_video)

    def test_has_document_paths_false(self):
        handler = DocumentImportFlowHandler()
        self.assertFalse(handler.has_document_paths())

    def test_has_document_paths_true(self):
        handler = DocumentImportFlowHandler(document_paths=ANY_PATHS)
        self.assertTrue(handler.has_document_paths())

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.ask_via_dialog_for_paths')
    def test_document_import_ask_for_paths(self, mocked_ask: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_ask.assert_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.import_paths')
    def test_document_import_import_paths(self, mocked_import: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_import.assert_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported')
    def test_document_import_no_paths_given(self, mocked_question: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_question.assert_not_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.have_comments', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.want_to_abort_the_import', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.want_to_clear_all_comments', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.ask_via_message_box_what_to_do_with_comments')
    def test_document_import_comments_question_with_comments(self, mocked_question: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_question.assert_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.have_comments', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.ask_via_message_box_what_to_do_with_comments')
    def test_document_import_comments_question_without_comments(self, mocked_question: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_question.assert_not_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.have_comments', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.ask_via_message_box_what_to_do_with_comments')
    @patch(f'{DOC_FLOW_ACTIONS}.want_to_abort_the_import', return_value=True)
    def test_document_import_has_abort_called(self, *_):
        handler = DocumentImportFlowHandler()
        self.assertFalse(handler.has_abort_called())
        handler.handle_flow_with(self.OPTIONS)
        self.assertTrue(handler.has_abort_called())

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.have_comments', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.ask_via_message_box_what_to_do_with_comments')
    @patch(f'{DOC_FLOW_ACTIONS}.want_to_abort_the_import', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.want_to_clear_all_comments', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.clear_all_comments', return_value=True)
    def test_document_import_clear_all_comments(self, mocked_clear: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_clear.assert_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.load_comments')
    def test_document_import_load_comments(self, mocked_load: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_load.assert_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_incompatibles_imported', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.show_via_message_box_all_incompatible_documents')
    def test_document_import_show_incompatibles(self, mocked_show: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_show.assert_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.get_the_found_videos', return_value=tuple([ANY_VIDEO]))
    @patch(f'{DOC_FLOW_ACTIONS}.get_all_paths_from_imported_documents', return_value=tuple([ANY_PATH]))
    @patch(f'{VID_FLOW_ACTIONS}.confirm_the_video_exists', return_value=True)
    @patch(f'{VID_FLOW_ACTIONS}.see_the_video_is_not_already_playing', return_value=True)
    @patch(f'{VID_FLOW_ACTIONS}.ask_via_message_box_to_open_found_video')
    @patch(f'{VID_FLOW_ACTIONS}.want_to_open_found_video', return_value=True)
    @patch(f'{VID_FLOW_ACTIONS}.load_video')
    def test_video_import_successful(self, mocked_load_video: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_load_video.assert_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.have_comments', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.ask_via_message_box_what_to_do_with_comments')
    @patch(f'{DOC_FLOW_ACTIONS}.want_to_abort_the_import', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.want_to_abort_the_import', return_value=True)
    @patch(VID_FLOW_ACTIONS)
    def test_video_import_skip_because_abort_called(self, mocked_constructor: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_constructor.assert_not_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.get_the_found_videos', return_value=tuple())
    @patch(VID_FLOW_ACTIONS)
    def test_video_import_skip_because_no_video_found(self, mocked_constructor: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_constructor.assert_not_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.get_all_paths_from_imported_documents', return_value=ANY_PATHS)
    @patch(VID_FLOW_ACTIONS)
    def test_video_import_skip_because_multiple_documents(self, mocked_constructor: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_constructor.assert_not_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.get_the_found_videos', return_value=tuple([ANY_VIDEO]))
    @patch(f'{DOC_FLOW_ACTIONS}.get_all_paths_from_imported_documents', return_value=tuple([ANY_PATH]))
    @patch(VID_FLOW_ACTIONS)
    def test_video_import_skip_because_skip_command(self, mocked_constructor: Mock, *_):
        handler = DocumentImportFlowHandler(load_linked_video=False)
        handler.handle_flow_with(self.OPTIONS)
        mocked_constructor.assert_not_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.get_the_found_videos', return_value=tuple([ANY_VIDEO]))
    @patch(f'{DOC_FLOW_ACTIONS}.get_all_paths_from_imported_documents', return_value=tuple([ANY_PATH]))
    @patch(f'{VID_FLOW_ACTIONS}.confirm_the_video_exists', return_value=False)
    @patch(f'{VID_FLOW_ACTIONS}.load_video')
    def test_video_import_skip_because_video_does_not_exist(self, mocked_load_video: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_load_video.assert_not_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.get_the_found_videos', return_value=tuple([ANY_VIDEO]))
    @patch(f'{DOC_FLOW_ACTIONS}.get_all_paths_from_imported_documents', return_value=tuple([ANY_PATH]))
    @patch(f'{VID_FLOW_ACTIONS}.confirm_the_video_exists', return_value=True)
    @patch(f'{VID_FLOW_ACTIONS}.see_the_video_is_not_already_playing', return_value=False)
    @patch(f'{VID_FLOW_ACTIONS}.load_video')
    def test_video_import_skip_because_video_is_playing_already(self, mocked_load_video: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_load_video.assert_not_called()

    @patch(f'{DOC_FLOW_ACTIONS}.dont_have_any_paths', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_any_paths', return_value=True)
    @patch(f'{DOC_FLOW_ACTIONS}.neither_have_documents_nor_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_documents_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.have_incompatibles_imported', return_value=False)
    @patch(f'{DOC_FLOW_ACTIONS}.get_the_found_videos', return_value=tuple([ANY_VIDEO]))
    @patch(f'{DOC_FLOW_ACTIONS}.get_all_paths_from_imported_documents', return_value=tuple([ANY_PATH]))
    @patch(f'{VID_FLOW_ACTIONS}.confirm_the_video_exists', return_value=True)
    @patch(f'{VID_FLOW_ACTIONS}.see_the_video_is_not_already_playing', return_value=False)
    @patch(f'{VID_FLOW_ACTIONS}.ask_via_message_box_to_open_found_video')
    @patch(f'{VID_FLOW_ACTIONS}.want_to_open_found_video', return_value=False)
    @patch(f'{VID_FLOW_ACTIONS}.load_video')
    def test_video_import_skip_because_user_doesnt_want_to_open(self, mocked_load_video: Mock, *_):
        handler = DocumentImportFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_load_video.assert_not_called()
