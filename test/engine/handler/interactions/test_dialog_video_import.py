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

from mpvqc.engine.handler.interactions import VideoImportDialog
from test.doc_io.input import ANY_VIDEO
from test.engine import AppTestImpl


class TestDialogVideoImport(unittest.TestCase):
    IMPORT_VIDEO = 'mpvqc.gui.filedialogs.Dialogs.import_video'
    EXPECTED = ANY_VIDEO

    @patch(IMPORT_VIDEO, return_value=EXPECTED)
    def test_get_video(self, *_) -> None:
        app = AppTestImpl()

        dialog = VideoImportDialog(app)
        actual = dialog.get_video()

        self.assertEqual(self.EXPECTED, actual)
