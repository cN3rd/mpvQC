import unittest
from unittest.mock import patch, Mock

from mpvqc.gui.messageboxes.impls import CouldNotSaveDocumentMessageBox


class TestCouldNotSaveDocumentMessageBox(unittest.TestCase):

    @patch('mpvqc.gui.messageboxes.impls.mb_could_not_save_document.QMessageBox')
    def test_messagebox_set_title(self, mocked_mb: Mock, *_):
        mb = CouldNotSaveDocumentMessageBox()
        mb.popup()

        mocked_mb.return_value.setWindowTitle.assert_called()

    @patch('mpvqc.gui.messageboxes.impls.mb_could_not_save_document.QMessageBox')
    def test_messagebox_set_text(self, mocked_mb: Mock):
        mb = CouldNotSaveDocumentMessageBox()
        mb.popup()

        mocked_mb.return_value.setText.assert_called()

    @patch('mpvqc.gui.messageboxes.impls.mb_could_not_save_document.QMessageBox')
    def test_messagebox_set_icon(self, mocked_mb: Mock):
        mb = CouldNotSaveDocumentMessageBox()
        mb.popup()

        mocked_mb.return_value.setIcon.assert_called()
