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

from mpvqc.engine.handler.interactions import IncompatibleDocumentsMessageBox
from test.doc_io.input import ANY_PATH
from test.engine import AppTestImpl


class TestMessageBoxIncompatibleDocuments(unittest.TestCase):
    INVALID_DOCUMENTS_DURING_IMPORT = 'mpvqc.gui.messageboxes.MessageBoxes.invalid_documents_during_import'

    INCOMPATIBLES = tuple([ANY_PATH])

    @patch(INVALID_DOCUMENTS_DURING_IMPORT)
    def test_show(self, mocked_func: Mock):
        app = AppTestImpl()

        dialog = IncompatibleDocumentsMessageBox(app)
        dialog.show()

        mocked_func.assert_called_once()

    @patch(INVALID_DOCUMENTS_DURING_IMPORT)
    def test_set_incompatibles(self, mocked_func: Mock):
        app = AppTestImpl()

        dialog = IncompatibleDocumentsMessageBox(app)
        dialog.set_incompatibles(self.INCOMPATIBLES)
        dialog.show()

        call_list = mocked_func.call_args_list
        first_call = call_list[0]
        incompatibles, _ = first_call.args

        self.assertEqual(self.INCOMPATIBLES, incompatibles)
