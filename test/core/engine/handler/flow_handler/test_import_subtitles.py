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

from mpvqc.core.engine.handler.flow_handler import SubtitleImportFlowHandler
from test.doc_io.input import ANY_PATHS
from test.core.engine import DEFAULT_OPTIONS


class Test(unittest.TestCase):
    FLOW_ACTIONS = 'mpvqc.core.engine.handler.flow_handler.import_subtitles.SubtitleImportFlowActions'

    def test_unchanged(self):
        handler = SubtitleImportFlowHandler()
        changes = handler.get_changes()
        self.assert_unchanged(changes)

    def assert_unchanged(self, changes):
        self.assertFalse(changes.cleared_the_table)
        self.assertFalse(changes.loaded_documents)
        self.assertFalse(changes.loaded_video)
        self.assertFalse(changes.stored_video)

    def test_has_subtitle_paths_true(self):
        handler = SubtitleImportFlowHandler(subtitle_paths=ANY_PATHS)
        self.assertTrue(handler.has_subtitle_paths())

    def test_has_subtitle_paths_false(self):
        handler = SubtitleImportFlowHandler()
        self.assertFalse(handler.has_subtitle_paths())

    @patch(f'{FLOW_ACTIONS}.dont_have_subtitles', return_value=True)
    @patch(f'{FLOW_ACTIONS}.ask_via_dialog_for_subtitles')
    def test_ask_for_subtitles_true(self, mocked_ask: Mock, *_):
        handler = SubtitleImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_ask.assert_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_subtitles', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_via_dialog_for_subtitles')
    def test_ask_for_subtitles_false(self, mocked_ask: Mock, *_):
        handler = SubtitleImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_ask.assert_not_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_subtitles', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_subtitles', return_value=True)
    @patch(f'{FLOW_ACTIONS}.load_subtitles')
    def test_load_subtitles_true(self, mocked_load: Mock, *_):
        handler = SubtitleImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_load.assert_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_subtitles', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_subtitles', return_value=False)
    @patch(f'{FLOW_ACTIONS}.load_subtitles')
    def test_load_subtitles_false(self, mocked_load: Mock, *_):
        handler = SubtitleImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_load.assert_not_called()
