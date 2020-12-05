import unittest
from unittest.mock import patch, Mock, ANY

from PyQt5.QtWidgets import QMessageBox

from mpvqc.gui.messageboxes import ExistingCommentsDuringImportMessageBox, ExistingCommentsDuringImportResponse


class TestExistingCommentsDuringImportMessageBox(unittest.TestCase):

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_set_title(self, mocked_mb: Mock, *_):
        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        mocked_mb.return_value.setWindowTitle.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_set_text(self, mocked_mb: Mock):
        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        mocked_mb.return_value.setText.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_set_icon(self, mocked_mb: Mock):
        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        mocked_mb.return_value.setIcon.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_set_button_cancel(self, mocked_mb: Mock):
        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(mocked_mb.Abort)

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_set_button_delete_comments(self, mocked_mb: Mock):
        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(ANY, mocked_mb.NoRole)

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_set_button_keep_comments(self, mocked_mb: Mock):
        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(ANY, mocked_mb.YesRole)

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_response_cancel_import(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = QMessageBox.Abort

        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        self.assertEqual(ExistingCommentsDuringImportResponse.CANCEL_IMPORT, mb.response())

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_response_delete_comments(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = 0

        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        self.assertEqual(ExistingCommentsDuringImportResponse.DELETE_COMMENTS, mb.response())

    @patch('mpvqc.gui.messageboxes.mb_existing_comments_during_import.QMessageBox')
    def test_messagebox_response_keep_comments(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = 1

        mb = ExistingCommentsDuringImportMessageBox()
        mb.popup()

        self.assertEqual(ExistingCommentsDuringImportResponse.KEEP_COMMENTS, mb.response())
