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

from mpvqc.engine.handler.flow_actions import SaveDocumentFlowActions
from mpvqc.engine.interface import Options
from test.doc_io.input import ANY_PATH
from test.engine import DEFAULT_OPTIONS, PlayerTestImpl, AppTestImpl, TableTestImpl


class TestSubtitleImportFlowActions(unittest.TestCase):
    DIALOG_ASK = 'mpvqc.engine.handler.flow_actions.save_document.SaveDialog.get_write_path'
    MB_SHOW_ERROR = 'mpvqc.engine.handler.flow_actions.save_document.SaveErrorMessageBox.show'

    WRITE = 'mpvqc.engine.handler.flow_actions.save_document.DocumentExporter.export'

    def test_dont_have_write_path(self):
        we = SaveDocumentFlowActions(DEFAULT_OPTIONS, current_file=None)
        self.assertFalse(we.have_write_path())
        self.assertTrue(we.dont_have_write_path())

    def test_have_write_path(self):
        we = SaveDocumentFlowActions(DEFAULT_OPTIONS, current_file=ANY_PATH)
        self.assertTrue(we.have_write_path())
        self.assertFalse(we.dont_have_write_path())

    def test_pause_called(self):
        player = PlayerTestImpl()
        options = Options(AppTestImpl(), player, TableTestImpl())

        we = SaveDocumentFlowActions(options, current_file=None)
        we.pause_video()

        self.assertTrue(player.pause_called)

    @patch(DIALOG_ASK)
    def test_ask_for_write_path(self, mocked_ask: Mock):
        we = SaveDocumentFlowActions(DEFAULT_OPTIONS, current_file=None)
        we.ask_user_via_dialog_for_write_path()
        mocked_ask.assert_called()
        self.assertTrue(we.have_write_path())

    @patch(WRITE)
    def test_write_called(self, mocked_write: Mock):
        we = SaveDocumentFlowActions(DEFAULT_OPTIONS, current_file=None)
        we.write_document()
        mocked_write.assert_called()

    @patch(WRITE)
    def test_write_changes_registered(self, *_):
        we = SaveDocumentFlowActions(DEFAULT_OPTIONS, current_file=ANY_PATH)
        self.assertFalse(we.get_changes().save_path)
        we.write_document()
        self.assertTrue(we.get_changes().save_path)

    @patch(MB_SHOW_ERROR)
    def test_show_error(self, mocked_error: Mock):
        we = SaveDocumentFlowActions(DEFAULT_OPTIONS, current_file=None)
        we.show_error()
        mocked_error.assert_called()
