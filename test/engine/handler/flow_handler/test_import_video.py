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

from mpvqc.engine.handler.flow_handler import VideoImportFlowHandler
from test.doc_io.input import ANY_VIDEO
from test.engine import DEFAULT_OPTIONS


class Test(unittest.TestCase):
    FLOW_ACTIONS = 'mpvqc.engine.handler.flow_handler.import_video.VideoImportFlowActions'

    def test_unchanged(self):
        handler = VideoImportFlowHandler()
        changes = handler.get_changes()
        self.assert_unchanged(changes)

    def assert_unchanged(self, changes):
        self.assertFalse(changes.cleared_the_table)
        self.assertFalse(changes.loaded_documents)
        self.assertFalse(changes.loaded_video)
        self.assertFalse(changes.stored_video)

    def test_has_video_path_true(self):
        handler = VideoImportFlowHandler()
        self.assertFalse(handler.has_video_path())

    def test_has_video_path_false(self):
        handler = VideoImportFlowHandler(video=ANY_VIDEO)
        self.assertTrue(handler.has_video_path())

    @patch(f'{FLOW_ACTIONS}.dont_have_a_video', return_value=True)
    @patch(f'{FLOW_ACTIONS}.ask_via_dialog_for_video')
    def test_ask_for_video_true(self, mocked_ask: Mock, *_):
        handler = VideoImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_ask.assert_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_a_video', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_via_dialog_for_video')
    def test_ask_for_video_false(self, mocked_ask: Mock, *_):
        handler = VideoImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_ask.assert_not_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_a_video', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_video', return_value=True)
    @patch(f'{FLOW_ACTIONS}.see_the_video_is_not_already_playing', return_value=True)
    @patch(f'{FLOW_ACTIONS}.load_video')
    def test_load_video_true(self, mocked_load: Mock, *_):
        handler = VideoImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_load.assert_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_a_video', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_video', return_value=True)
    @patch(f'{FLOW_ACTIONS}.see_the_video_is_not_already_playing', return_value=True)
    def test_load_video_changes_registered(self, *_):
        handler = VideoImportFlowHandler(video=ANY_VIDEO)
        self.assertIsNone(handler.get_changes().loaded_video)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        self.assertIsNotNone(handler.get_changes().loaded_video)

    @patch(f'{FLOW_ACTIONS}.dont_have_a_video', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_video', return_value=False)
    @patch(f'{FLOW_ACTIONS}.load_video')
    def test_load_video_false_because_dont_have_video(self, mocked_load: Mock, *_):
        handler = VideoImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_load.assert_not_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_a_video', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_video', return_value=True)
    @patch(f'{FLOW_ACTIONS}.see_the_video_is_not_already_playing', return_value=False)
    @patch(f'{FLOW_ACTIONS}.load_video')
    def test_load_video_false_because_already_playing(self, mocked_load: Mock, *_):
        handler = VideoImportFlowHandler()
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_load.assert_not_called()
