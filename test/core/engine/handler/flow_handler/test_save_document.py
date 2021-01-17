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

from mpvqc.core.engine.handler.flow_handler import SaveDocumentFlowHandler
from test.doc_io.input import ANY_PATH
from test.core.engine import DEFAULT_OPTIONS


class Test(unittest.TestCase):
    FLOW_ACTIONS = 'mpvqc.core.engine.handler.flow_handler.save_document.SaveDocumentFlowActions'

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=True)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_user_via_dialog_for_write_path')
    def test_ask_for_write_path_true(self, mocked_ask: Mock, *_):
        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_ask.assert_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=True)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_user_via_dialog_for_write_path')
    @patch(f'{FLOW_ACTIONS}.pause_video')
    def test_ask_for_write_path_true_pause_called(self, mocked_pause: Mock, *_):
        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_pause.assert_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_user_via_dialog_for_write_path')
    def test_ask_for_write_path_false(self, mocked_ask: Mock, *_):
        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_ask.assert_not_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_user_via_dialog_for_write_path')
    @patch(f'{FLOW_ACTIONS}.pause_video')
    def test_ask_for_write_path_false_pause_not_called(self, mocked_pause: Mock, *_):
        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_pause.assert_not_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=True)
    @patch(f'{FLOW_ACTIONS}.write_document')
    def test_write_document_true(self, mocked_write: Mock, *_):
        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_write.assert_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=True)
    @patch('mpvqc.core.engine.handler.flow_actions.save_document.DocumentExporter.export')
    def test_write_document_true_changes_registered(self, *_):
        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        self.assertIsNone(handler.get_changes().save_path)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        self.assertIsNotNone(handler.get_changes().save_path)

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.write_document')
    def test_write_document_false(self, mocked_write: Mock, *_):
        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_write.assert_not_called()

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=False)
    def test_write_document_false_changes_not_registered(self, *_):
        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        self.assertIsNone(handler.get_changes().save_path)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        self.assertIsNone(handler.get_changes().save_path)

    @patch(f'{FLOW_ACTIONS}.dont_have_write_path', return_value=False)
    @patch(f'{FLOW_ACTIONS}.have_write_path', return_value=True)
    @patch(f'{FLOW_ACTIONS}.write_document')
    @patch(f'{FLOW_ACTIONS}.show_error')
    def test_error_shown(self, mocked_error: Mock, mocked_write: Mock, *_):
        def not_this_time():
            raise ValueError("Permission error :(")

        mocked_write.side_effect = not_this_time

        handler = SaveDocumentFlowHandler(current_file=ANY_PATH)
        handler.handle_flow_with(DEFAULT_OPTIONS)
        mocked_error.assert_called()
