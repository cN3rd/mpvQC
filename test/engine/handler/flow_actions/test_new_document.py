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

from mpvqc.engine.handler.flow_actions import NewDocumentFlowActions
from test.engine import DEFAULT_OPTIONS


class TestSubtitleImportFlowActions(unittest.TestCase):
    MB_CREATE_NEW_ASK = 'mpvqc.engine.handler.flow_actions.new_document.NewDocumentMessageBox.ask'
    MB_CREATE_NEW_DO_WE = 'mpvqc.engine.handler.flow_actions.new_document.NewDocumentMessageBox.do_we_create_new'

    CLEAR = 'mpvqc.engine.handler.flow_actions.new_document.TableClearer.clear_table'

    def test_have_unsaved_changes(self):
        we = NewDocumentFlowActions(DEFAULT_OPTIONS, have_unsaved_changes=True)
        self.assertTrue(we.have_unsaved_changes())

    def test_dont_have_unsaved_changes(self):
        we = NewDocumentFlowActions(DEFAULT_OPTIONS, have_unsaved_changes=False)
        self.assertFalse(we.have_unsaved_changes())

    @patch(MB_CREATE_NEW_ASK)
    def test_ask_to_create_new_document(self, mocked_ask: Mock):
        we = NewDocumentFlowActions(DEFAULT_OPTIONS, have_unsaved_changes=True)
        we.ask_via_message_box_to_create_new_document()
        mocked_ask.assert_called()

    @patch(MB_CREATE_NEW_DO_WE)
    def test_do_we_create_new(self, mocked_do_we: Mock):
        we = NewDocumentFlowActions(DEFAULT_OPTIONS, have_unsaved_changes=True)
        we.want_to_create_new_document()
        mocked_do_we.assert_called()

    @patch(CLEAR)
    def test_clear_table_called(self, mocked_clear: Mock):
        we = NewDocumentFlowActions(DEFAULT_OPTIONS, have_unsaved_changes=True)
        we.clear_comments()
        mocked_clear.assert_called()

    @patch(CLEAR)
    def test_clear_changes_registered(self, *_):
        we = NewDocumentFlowActions(DEFAULT_OPTIONS, have_unsaved_changes=True)
        we.clear_comments()
        self.assertTrue(we.get_changes().cleared_the_table)
