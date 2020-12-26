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

from mpvqc.engine.handler.interactions import SubtitleImportDialog
from test.doc_io.input import ANY_PATH
from test.engine import AppTestImpl


class TestDialogSubtitlesImport(unittest.TestCase):
    IMPORT_SUBTITLES = 'mpvqc.gui.filedialogs.Dialogs.import_subtitles'
    EXPECTED = tuple([ANY_PATH, ANY_PATH, ANY_PATH])

    @patch(IMPORT_SUBTITLES, return_value=EXPECTED)
    def test_get_subtitles(self, *_) -> None:
        app = AppTestImpl()

        dialog = SubtitleImportDialog(app)
        actual = dialog.get_subtitles()

        self.assertEqual(self.EXPECTED, actual)
