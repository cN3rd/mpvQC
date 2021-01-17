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

from mpvqc.core.engine.handler.interactions import VideoFoundMessageBox
from mpvqc.gui.messageboxes import ValidVideoFileFoundResponse
from test.core.engine import AppTestImpl


class TestMessageBoxNewDocuments(unittest.TestCase):
    VALID_VIDEO_FOUND = 'mpvqc.gui.messageboxes.MessageBoxes.valid_video_found'

    EXPECTED_NOT_OPEN = ValidVideoFileFoundResponse.NOT_OPEN
    EXPECTED_OPEN = ValidVideoFileFoundResponse.OPEN

    @patch(VALID_VIDEO_FOUND, return_value=EXPECTED_NOT_OPEN)
    def test_ask(self, mocked_func: Mock):
        app = AppTestImpl()

        dialog = VideoFoundMessageBox(app)
        dialog.ask()

        mocked_func.assert_called_once()

    @patch(VALID_VIDEO_FOUND, return_value=EXPECTED_OPEN)
    def test_open(self, *_):
        app = AppTestImpl()

        dialog = VideoFoundMessageBox(app)
        dialog.ask()

        self.assertTrue(dialog.do_we_open())

    @patch(VALID_VIDEO_FOUND, return_value=EXPECTED_NOT_OPEN)
    def test_not_open(self, *_):
        app = AppTestImpl()

        dialog = VideoFoundMessageBox(app)
        dialog.ask()

        self.assertFalse(dialog.do_we_open())
