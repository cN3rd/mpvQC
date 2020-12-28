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
from unittest.mock import patch

from mpvqc.engine.handler.interactions import QuitUnsavedMessageBox
from mpvqc.gui.messageboxes import UnsavedChangesQuitResponse
from test.engine import AppTestImpl


class TestMessageBoxQuitUnsaved(unittest.TestCase):
    UNSAVED_CHANGES_QUIT = 'mpvqc.gui.messageboxes.MessageBoxes.unsaved_changes_quit'

    EXPECTED_QUIT = UnsavedChangesQuitResponse.QUIT
    EXPECTED_CANCEL = UnsavedChangesQuitResponse.CANCEL

    @patch(UNSAVED_CHANGES_QUIT, return_value=EXPECTED_CANCEL)
    def test_cancel(self, *_):
        app = AppTestImpl()

        dialog = QuitUnsavedMessageBox(app)

        self.assertFalse(dialog.do_we_quit())

    @patch(UNSAVED_CHANGES_QUIT, return_value=EXPECTED_QUIT)
    def test_quit(self, *_):
        app = AppTestImpl()

        dialog = QuitUnsavedMessageBox(app)

        self.assertTrue(dialog.do_we_quit())
