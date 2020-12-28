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

from mpvqc.engine.handler.interactions import SaveErrorMessageBox
from test.engine import AppTestImpl


class TestMessageBoxIncompatibleDocuments(unittest.TestCase):
    COULD_NOT_SAVE_DOCUMENT = 'mpvqc.gui.messageboxes.MessageBoxes.could_not_save_document'

    @patch(COULD_NOT_SAVE_DOCUMENT)
    def test_show(self, mocked_func: Mock):
        app = AppTestImpl()

        dialog = SaveErrorMessageBox(app)
        dialog.show()

        mocked_func.assert_called_once()
