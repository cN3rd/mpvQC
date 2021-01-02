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

from mpvqc.engine.handler.flow_handler import NewDocumentFlowHandler
from mpvqc.engine.interface import Options
from test.engine import PlayerTestImpl, AppTestImpl, TableTestImpl


class Test(unittest.TestCase):
    FLOW_ACTIONS = 'mpvqc.engine.handler.flow_handler.new_document.NewDocumentFlowActions'

    OPTIONS = Options(
        AppTestImpl(),
        PlayerTestImpl(),
        TableTestImpl()
    )

    def test_unchanged(self):
        handler = NewDocumentFlowHandler(have_unsaved_changes=False)
        changes = handler.get_changes()
        self.assertFalse(changes.cleared_the_table)

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=True)
    @patch(f'{FLOW_ACTIONS}.want_to_create_new_document', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_via_message_box_to_create_new_document')
    def test_ask_to_create_new_true(self, mocked_ask: Mock, *_):
        handler = NewDocumentFlowHandler(have_unsaved_changes=False)
        handler.handle_flow_with(self.OPTIONS)
        mocked_ask.assert_called()

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_via_message_box_to_create_new_document')
    def test_ask_to_create_new_false(self, mocked_ask: Mock, *_):
        handler = NewDocumentFlowHandler(have_unsaved_changes=False)
        handler.handle_flow_with(self.OPTIONS)
        mocked_ask.assert_not_called()

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=True)
    @patch(f'{FLOW_ACTIONS}.ask_via_message_box_to_create_new_document')
    @patch(f'{FLOW_ACTIONS}.want_to_create_new_document', return_value=True)
    @patch(f'{FLOW_ACTIONS}.clear_comments')
    def test_user_wants_to_create_new_true(self, mocked_clear: Mock, *_):
        handler = NewDocumentFlowHandler(have_unsaved_changes=False)
        handler.handle_flow_with(self.OPTIONS)
        mocked_clear.assert_called()

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=True)
    @patch(f'{FLOW_ACTIONS}.ask_via_message_box_to_create_new_document')
    @patch(f'{FLOW_ACTIONS}.want_to_create_new_document', return_value=True)
    def test_user_wants_to_create_new_true_changes_registered(self, *_):
        handler = NewDocumentFlowHandler(have_unsaved_changes=False)
        self.assertFalse(handler.get_changes().cleared_the_table)
        handler.handle_flow_with(self.OPTIONS)
        self.assertTrue(handler.get_changes().cleared_the_table)

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=True)
    @patch(f'{FLOW_ACTIONS}.ask_via_message_box_to_create_new_document')
    @patch(f'{FLOW_ACTIONS}.want_to_create_new_document', return_value=False)
    @patch(f'{FLOW_ACTIONS}.clear_comments')
    def test_user_wants_to_create_new_false(self, mocked_clear: Mock, *_):
        handler = NewDocumentFlowHandler(have_unsaved_changes=False)
        handler.handle_flow_with(self.OPTIONS)
        mocked_clear.assert_not_called()

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=False)
    @patch(f'{FLOW_ACTIONS}.clear_comments')
    def test_dont_have_unsaved_changes(self, mocked_clear: Mock, *_):
        handler = NewDocumentFlowHandler(have_unsaved_changes=False)
        handler.handle_flow_with(self.OPTIONS)
        mocked_clear.assert_called()

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=False)
    def test_dont_have_unsaved_changes_changes_registered(self, *_):
        handler = NewDocumentFlowHandler(have_unsaved_changes=False)
        self.assertFalse(handler.get_changes().cleared_the_table)
        handler.handle_flow_with(self.OPTIONS)
        self.assertTrue(handler.get_changes().cleared_the_table)
