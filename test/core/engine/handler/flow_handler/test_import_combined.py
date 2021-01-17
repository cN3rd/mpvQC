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

from mpvqc.core.engine.handler.flow_handler import CombinedImportFlowHandler
from mpvqc.core.engine.states import ImportChanges
from test.doc_io.input import ANY_PATHS, ANY_VIDEO
from test.core.engine import DEFAULT_OPTIONS

IMPORT_CHANGES_DOCUMENT = ImportChanges()
IMPORT_CHANGES_DOCUMENT.loaded_documents = ANY_PATHS
IMPORT_CHANGES_DOCUMENT.stored_video = ANY_VIDEO

IMPORT_CHANGES_VIDEO = ImportChanges()
IMPORT_CHANGES_VIDEO.loaded_video = ANY_VIDEO


class Test(unittest.TestCase):
    DOCUMENT_HANDLER = 'mpvqc.core.engine.handler.flow_handler.import_combined.DocumentImportFlowHandler'
    SUBTITLE_HANDLER = 'mpvqc.core.engine.handler.flow_handler.import_combined.SubtitleImportFlowHandler'
    VIDEO_HANDLER = 'mpvqc.core.engine.handler.flow_handler.import_combined.VideoImportFlowHandler'

    def test_unchanged(self):
        handler = CombinedImportFlowHandler()
        changes = handler.get_changes()
        self.assert_unchanged(changes)

    def assert_unchanged(self, changes):
        self.assertFalse(changes.cleared_the_table)
        self.assertFalse(changes.loaded_documents)
        self.assertFalse(changes.loaded_video)
        self.assertFalse(changes.stored_video)

    @patch(f'{DOCUMENT_HANDLER}.handle_flow_with')
    @patch(f'{DOCUMENT_HANDLER}.has_document_paths', return_value=True)
    @patch(f'{DOCUMENT_HANDLER}.has_abort_called', return_value=True)
    @patch(VIDEO_HANDLER)
    def test_abort(self, mocked_video_handler: Mock, *_):
        handler = CombinedImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_video_handler.assert_not_called()

    def test_load_video_from_document_true(self):
        handler = CombinedImportFlowHandler()
        self.assertTrue(handler.only_if_user_has_not_supplied_a_video())

    def test_load_video_from_document_false(self):
        handler = CombinedImportFlowHandler(video_path=ANY_VIDEO)
        self.assertFalse(handler.only_if_user_has_not_supplied_a_video())

    @patch(f'{DOCUMENT_HANDLER}.has_document_paths', return_value=False)
    @patch(f'{DOCUMENT_HANDLER}.handle_flow_with')
    def test_import_only_when_paths_given_for_documents(self, mocked_handle: Mock, *_):
        handler = CombinedImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_handle.assert_not_called()

    @patch(f'{VIDEO_HANDLER}.has_video_path', return_value=False)
    @patch(f'{VIDEO_HANDLER}.handle_flow_with')
    def test_import_only_when_paths_given_for_videos(self, mocked_handle: Mock, *_):
        handler = CombinedImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_handle.assert_not_called()

    @patch(f'{SUBTITLE_HANDLER}.has_subtitle_paths', return_value=False)
    @patch(f'{SUBTITLE_HANDLER}.handle_flow_with')
    def test_import_only_when_paths_given_for_subtitles(self, mocked_handle: Mock, *_):
        handler = CombinedImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_handle.assert_not_called()

    @patch(f'{DOCUMENT_HANDLER}.has_document_paths', return_value=True)
    @patch(f'{DOCUMENT_HANDLER}.handle_flow_with')
    @patch(f'{DOCUMENT_HANDLER}.has_abort_called', return_value=False)
    @patch(f'{DOCUMENT_HANDLER}.get_changes', return_value=IMPORT_CHANGES_DOCUMENT)
    def test_document_import(self, *_):
        handler = CombinedImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        changes = handler.get_changes()
        self.assertTrue(changes.loaded_documents)

    @patch(f'{VIDEO_HANDLER}.has_video_path', return_value=True)
    @patch(f'{VIDEO_HANDLER}.handle_flow_with')
    @patch(f'{VIDEO_HANDLER}.get_changes', return_value=IMPORT_CHANGES_VIDEO)
    def test_video_import(self, *_):
        handler = CombinedImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        changes = handler.get_changes()
        self.assertTrue(changes.loaded_video)

    @patch(f'{DOCUMENT_HANDLER}.has_document_paths', return_value=True)
    @patch(f'{DOCUMENT_HANDLER}.handle_flow_with')
    @patch(f'{DOCUMENT_HANDLER}.has_abort_called', return_value=False)
    @patch(f'{DOCUMENT_HANDLER}.get_changes', return_value=IMPORT_CHANGES_DOCUMENT)
    @patch(f'{VIDEO_HANDLER}.has_video_path', return_value=True)
    @patch(f'{VIDEO_HANDLER}.handle_flow_with')
    @patch(f'{VIDEO_HANDLER}.get_changes', return_value=IMPORT_CHANGES_VIDEO)
    def test_document_and_video_import(self, *_):
        handler = CombinedImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        changes = handler.get_changes()
        self.assertTrue(changes.loaded_documents)
        self.assertTrue(changes.loaded_video)
