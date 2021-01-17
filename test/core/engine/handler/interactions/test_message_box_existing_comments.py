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

from mpvqc.core.engine.handler.interactions import ExistingCommentsMessageBox
from mpvqc.gui.messageboxes import ExistingCommentsDuringImportResponse
from test.core.engine import AppTestImpl


class TestMessageBoxExistingComments(unittest.TestCase):
    EXISTING_COMMENTS_DURING_IMPORT = 'mpvqc.gui.messageboxes.MessageBoxes.existing_comments_during_import'

    EXPECTED_CANCEL = ExistingCommentsDuringImportResponse.CANCEL_IMPORT
    EXPECTED_KEEP = ExistingCommentsDuringImportResponse.KEEP_COMMENTS
    EXPECTED_DELETE = ExistingCommentsDuringImportResponse.DELETE_COMMENTS

    @patch(EXISTING_COMMENTS_DURING_IMPORT, return_value=EXPECTED_CANCEL)
    def test_ask(self, mocked_func: Mock):
        app = AppTestImpl()

        dialog = ExistingCommentsMessageBox(app)
        dialog.ask()

        mocked_func.assert_called_once()

    @patch(EXISTING_COMMENTS_DURING_IMPORT, return_value=EXPECTED_CANCEL)
    def test_cancel_import(self, *_):
        app = AppTestImpl()

        dialog = ExistingCommentsMessageBox(app)
        dialog.ask()

        self.assertTrue(dialog.do_we_abort())

    @patch(EXISTING_COMMENTS_DURING_IMPORT, return_value=EXPECTED_DELETE)
    def test_delete_comments(self, *_):
        app = AppTestImpl()

        dialog = ExistingCommentsMessageBox(app)
        dialog.ask()

        self.assertTrue(dialog.do_we_clear_table())

    @patch(EXISTING_COMMENTS_DURING_IMPORT, return_value=EXPECTED_KEEP)
    def test_keep_comments(self, *_):
        app = AppTestImpl()

        dialog = ExistingCommentsMessageBox(app)
        dialog.ask()

        self.assertFalse(dialog.do_we_abort())
        self.assertFalse(dialog.do_we_clear_table())
