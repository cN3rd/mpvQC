import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from mpvqc.gui.messageboxes.impls import InvalidDocumentDuringImportMessageBox


class TestInvalidDocumentDuringImportMessageBox(unittest.TestCase):
    SINGLE_PATH = tuple([Path.home()])
    MULTI_PATH = tuple([Path.home(), Path.home()])

    @patch('mpvqc.gui.messageboxes.impls.mb_invalid_document_during_import.QMessageBox')
    def test_messagebox_set_title(self, mocked_mb: Mock, *_):
        mb = InvalidDocumentDuringImportMessageBox(self.MULTI_PATH)
        mb.popup()

        mocked_mb.return_value.setWindowTitle.assert_called()

    @patch('mpvqc.gui.messageboxes.impls.mb_invalid_document_during_import.QMessageBox')
    def test_messagebox_set_text(self, mocked_mb: Mock):
        mb = InvalidDocumentDuringImportMessageBox(self.SINGLE_PATH)
        mb.popup()

        mocked_mb.return_value.setText.assert_called()

    @patch('mpvqc.gui.messageboxes.impls.mb_invalid_document_during_import.QMessageBox')
    def test_messagebox_set_informative_text(self, mocked_mb: Mock):
        mb = InvalidDocumentDuringImportMessageBox(self.MULTI_PATH)
        mb.popup()

        mocked_mb.return_value.setInformativeText.assert_called()

    @patch('mpvqc.gui.messageboxes.impls.mb_invalid_document_during_import.QMessageBox')
    def test_messagebox_set_icon(self, mocked_mb: Mock):
        mb = InvalidDocumentDuringImportMessageBox(self.SINGLE_PATH)
        mb.popup()

        mocked_mb.return_value.setIcon.assert_called()
