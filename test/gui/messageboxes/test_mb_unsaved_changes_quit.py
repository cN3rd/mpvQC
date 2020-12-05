import unittest
from unittest.mock import patch, Mock

from PyQt5.QtWidgets import QMessageBox

from mpvqc.gui.messageboxes import UnsavedChangesQuitMessageBox, UnsavedChangesQuitResponse


class TestUnsavedChangesQuitMessageBox(unittest.TestCase):

    @patch('mpvqc.gui.messageboxes.mb_unsaved_changes_quit.QMessageBox')
    def test_messagebox_set_title(self, mocked_mb: Mock, *_):
        mb = UnsavedChangesQuitMessageBox()
        mb.popup()

        mocked_mb.return_value.setWindowTitle.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_unsaved_changes_quit.QMessageBox')
    def test_messagebox_set_text(self, mocked_mb: Mock):
        mb = UnsavedChangesQuitMessageBox()
        mb.popup()

        mocked_mb.return_value.setText.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_unsaved_changes_quit.QMessageBox')
    def test_messagebox_set_icon(self, mocked_mb: Mock):
        mb = UnsavedChangesQuitMessageBox()
        mb.popup()

        mocked_mb.return_value.setIcon.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_unsaved_changes_quit.QMessageBox')
    def test_messagebox_set_button_quit(self, mocked_mb: Mock):
        mb = UnsavedChangesQuitMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(mocked_mb.Yes)

    @patch('mpvqc.gui.messageboxes.mb_unsaved_changes_quit.QMessageBox')
    def test_messagebox_set_button_cancel(self, mocked_mb: Mock):
        mb = UnsavedChangesQuitMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(mocked_mb.No)

    @patch('mpvqc.gui.messageboxes.mb_unsaved_changes_quit.QMessageBox')
    def test_messagebox_response_quit(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = QMessageBox.Yes

        mb = UnsavedChangesQuitMessageBox()
        mb.popup()

        self.assertEqual(UnsavedChangesQuitResponse.QUIT, mb.response())

    @patch('mpvqc.gui.messageboxes.mb_unsaved_changes_quit.QMessageBox')
    def test_messagebox_response_cancel(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = QMessageBox.No

        mb = UnsavedChangesQuitMessageBox()
        mb.popup()

        self.assertEqual(UnsavedChangesQuitResponse.CANCEL, mb.response())
