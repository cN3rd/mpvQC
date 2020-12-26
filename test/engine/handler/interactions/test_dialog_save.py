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

from mpvqc.engine.handler.interactions import SaveDialog
from test import MockedSettings
from test.doc_io.input import ANY_PATH, ANY_VIDEO
from test.engine import AppTestImpl


class TestDialogDocumentImport(unittest.TestCase):
    GET_SETTINGS = 'mpvqc.engine.handler.interactions.dialog_save.get_settings'
    EXPORT_DOCUMENT = 'mpvqc.gui.filedialogs.Dialogs.export_document'

    @patch(GET_SETTINGS, return_value=MockedSettings())
    @patch(EXPORT_DOCUMENT, return_value=ANY_PATH)
    def test_set_any_video(self, mocked_export_document: Mock, *_) -> None:
        app = AppTestImpl()
        dialog = SaveDialog(app)
        dialog.set_video(ANY_VIDEO)
        dialog.get_write_path()

        call_list = mocked_export_document.call_args_list
        first_call = call_list[0]
        path_suggestion, _ = first_call.args

        self.assertIn(ANY_VIDEO.stem, str(path_suggestion))

    @patch(GET_SETTINGS, return_value=MockedSettings())
    @patch(EXPORT_DOCUMENT, return_value=ANY_PATH)
    def test_set_no_video(self, mocked_export_document: Mock, *_) -> None:
        app = AppTestImpl()
        dialog = SaveDialog(app)
        dialog.get_write_path()

        call_list = mocked_export_document.call_args_list
        first_call = call_list[0]
        path_suggestion, _ = first_call.args

        self.assertIn('untitled', str(path_suggestion))

    @patch(GET_SETTINGS, return_value=MockedSettings())
    @patch(EXPORT_DOCUMENT, return_value=ANY_PATH)
    def test_get_write_path(self, *_) -> None:
        app = AppTestImpl()

        dialog = SaveDialog(app)
        actual = dialog.get_write_path()

        self.assertEqual(ANY_PATH, actual)
