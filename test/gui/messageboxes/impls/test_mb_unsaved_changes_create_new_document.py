import unittest
from unittest.mock import patch, Mock

from PyQt5.QtWidgets import QMessageBox

from mpvqc.gui.messageboxes.impls import UnsavedChangesCreateNewDocumentMessageBox, UnsavedChangesCreateNewDocumentResponse


class TestUnsavedChangesCreateNewDocumentMessageBox(unittest.TestCase):

    @patch('mpvqc.gui.messageboxes.impls.mb_unsaved_changes_create_new_document.QMessageBox')
    def test_messagebox_set_title(self, mocked_mb: Mock, *_):
        mb = UnsavedChangesCreateNewDocumentMessageBox()
        mb.popup()

        mocked_mb.return_value.setWindowTitle.assert_called()

    @patch('mpvqc.gui.messageboxes.impls.mb_unsaved_changes_create_new_document.QMessageBox')
    def test_messagebox_set_text(self, mocked_mb: Mock):
        mb = UnsavedChangesCreateNewDocumentMessageBox()
        mb.popup()

        mocked_mb.return_value.setText.assert_called()

    @patch('mpvqc.gui.messageboxes.impls.mb_unsaved_changes_create_new_document.QMessageBox')
    def test_messagebox_set_icon(self, mocked_mb: Mock):
        mb = UnsavedChangesCreateNewDocumentMessageBox()
        mb.popup()

        mocked_mb.return_value.setIcon.assert_called()

    @patch('mpvqc.gui.messageboxes.impls.mb_unsaved_changes_create_new_document.QMessageBox')
    def test_messagebox_set_button_create_new(self, mocked_mb: Mock):
        mb = UnsavedChangesCreateNewDocumentMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(mocked_mb.Yes)

    @patch('mpvqc.gui.messageboxes.impls.mb_unsaved_changes_create_new_document.QMessageBox')
    def test_messagebox_set_button_cancel(self, mocked_mb: Mock):
        mb = UnsavedChangesCreateNewDocumentMessageBox()
        mb.popup()

        mocked_mb.return_value.addButton.assert_any_call(mocked_mb.No)

    @patch('mpvqc.gui.messageboxes.impls.mb_unsaved_changes_create_new_document.QMessageBox')
    def test_messagebox_response_create_new(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = QMessageBox.Yes

        mb = UnsavedChangesCreateNewDocumentMessageBox()
        mb.popup()

        self.assertEqual(UnsavedChangesCreateNewDocumentResponse.CREATE_NEW, mb.response())

    @patch('mpvqc.gui.messageboxes.impls.mb_unsaved_changes_create_new_document.QMessageBox')
    def test_messagebox_response_cancel(self, mocked_mb: Mock):
        mocked_mb.return_value.exec_.return_value = QMessageBox.No

        mb = UnsavedChangesCreateNewDocumentMessageBox()
        mb.popup()

        self.assertEqual(UnsavedChangesCreateNewDocumentResponse.CANCEL, mb.response())
