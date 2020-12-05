import unittest
from unittest.mock import patch, Mock

from PyQt5.QtWidgets import QMessageBox

from mpvqc.gui.messageboxes import ValidVideoFileFoundMessageBox, ValidVideoFileFoundResponse


class TestValidVideoFileFoundMessageBox(unittest.TestCase):

    @patch('mpvqc.gui.messageboxes.mb_valid_video_file_found.QMessageBox')
    def test_messagebox_set_title(self, mocked_mb: Mock, *_):
        mb = ValidVideoFileFoundMessageBox()
        mb.popup()

        mocked_mb.return_value.setWindowTitle.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_valid_video_file_found.QMessageBox')
    def test_messagebox_set_text(self, mocked_mb: Mock):
        mb = ValidVideoFileFoundMessageBox()
        mb.popup()

        mocked_mb.return_value.setText.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_valid_video_file_found.QMessageBox')
    def test_messagebox_set_icon(self, mocked_mb: Mock):
        mb = ValidVideoFileFoundMessageBox()
        mb.popup()

        mocked_mb.return_value.setIcon.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_valid_video_file_found.QMessageBox')
    def test_messagebox_set_button_open(self, mocked_mb: Mock):
        mb = ValidVideoFileFoundMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(mocked_mb.Yes)

    @patch('mpvqc.gui.messageboxes.mb_valid_video_file_found.QMessageBox')
    def test_messagebox_set_button_not_open(self, mocked_mb: Mock):
        mb = ValidVideoFileFoundMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(mocked_mb.No)

    @patch('mpvqc.gui.messageboxes.mb_valid_video_file_found.QMessageBox')
    def test_messagebox_response_open(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = QMessageBox.Yes

        mb = ValidVideoFileFoundMessageBox()
        mb.popup()

        self.assertEqual(ValidVideoFileFoundResponse.OPEN, mb.response())

    @patch('mpvqc.gui.messageboxes.mb_valid_video_file_found.QMessageBox')
    def test_messagebox_response_not_open(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = QMessageBox.No

        mb = ValidVideoFileFoundMessageBox()
        mb.popup()

        self.assertEqual(ValidVideoFileFoundResponse.NOT_OPEN, mb.response())
