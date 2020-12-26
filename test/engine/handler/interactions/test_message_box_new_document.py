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

from mpvqc.engine.handler.interactions import NewDocumentMessageBox
from mpvqc.gui.messageboxes import UnsavedChangesCreateNewDocumentResponse
from test.engine import AppTestImpl


class TestMessageBoxNewDocuments(unittest.TestCase):
    UNSAVED_CHANGES_CREATE_NEW_DOCUMENT = 'mpvqc.gui.messageboxes.MessageBoxes.unsaved_changes_create_new_document'

    EXPECTED_CREATE_NEW = UnsavedChangesCreateNewDocumentResponse.CREATE_NEW
    EXPECTED_CANCEL = UnsavedChangesCreateNewDocumentResponse.CANCEL

    @patch(UNSAVED_CHANGES_CREATE_NEW_DOCUMENT, return_value=EXPECTED_CREATE_NEW)
    def test_ask(self, mocked_func: Mock) -> None:
        app = AppTestImpl()

        dialog = NewDocumentMessageBox(app)
        dialog.ask()

        mocked_func.assert_called_once()

    @patch(UNSAVED_CHANGES_CREATE_NEW_DOCUMENT, return_value=EXPECTED_CANCEL)
    def test_cancel(self, *_) -> None:
        app = AppTestImpl()

        dialog = NewDocumentMessageBox(app)
        dialog.ask()

        self.assertFalse(dialog.do_we_create_new())

    @patch(UNSAVED_CHANGES_CREATE_NEW_DOCUMENT, return_value=EXPECTED_CREATE_NEW)
    def test_create_new(self, *_) -> None:
        app = AppTestImpl()

        dialog = NewDocumentMessageBox(app)
        dialog.ask()

        self.assertTrue(dialog.do_we_create_new())
