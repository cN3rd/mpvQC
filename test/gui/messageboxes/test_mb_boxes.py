import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from mpvqc.gui.messageboxes.impls import \
    ExistingCommentsDuringImportResponse, \
    UnsavedChangesCreateNewDocumentResponse, \
    UnsavedChangesQuitResponse, \
    ValidVideoFileFoundResponse
from mpvqc.gui.messageboxes.mb_boxes import MessageBoxes


class TestMessageBoxes(unittest.TestCase):

    @patch('mpvqc.gui.messageboxes.mb_boxes.CouldNotSaveDocumentMessageBox')
    def test_could_not_save_document_popup(self, mocked_box: Mock, *_):
        MessageBoxes.could_not_save_document()
        mocked_box.return_value.popup.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_boxes.ExistingCommentsDuringImportMessageBox')
    def test_existing_comments_during_import_popup(self, mocked_box: Mock, *_):
        MessageBoxes.existing_comments_during_import()
        mocked_box.return_value.popup.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_boxes.ExistingCommentsDuringImportMessageBox')
    def test_existing_comments_during_import_response(self, mocked_box: Mock, *_):
        expected = ExistingCommentsDuringImportResponse.DELETE_COMMENTS
        mocked_box.return_value.response.return_value = expected
        actual = MessageBoxes.existing_comments_during_import()

        self.assertEqual(expected, actual)

    @patch('mpvqc.gui.messageboxes.mb_boxes.InvalidDocumentDuringImportMessageBox')
    def test_invalid_documents_during_import_popup(self, mocked_box: Mock, *_):
        MessageBoxes.invalid_documents_during_import(tuple([Path.home()]))
        mocked_box.return_value.popup.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_boxes.UnsavedChangesCreateNewDocumentMessageBox')
    def test_unsaved_changes_create_new_document_popup(self, mocked_box: Mock, *_):
        MessageBoxes.unsaved_changes_create_new_document()
        mocked_box.return_value.popup.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_boxes.UnsavedChangesCreateNewDocumentMessageBox')
    def test_unsaved_changes_create_new_document_response(self, mocked_box: Mock, *_):
        expected = UnsavedChangesCreateNewDocumentResponse.CREATE_NEW
        mocked_box.return_value.response.return_value = expected
        actual = MessageBoxes.unsaved_changes_create_new_document()

        self.assertEqual(expected, actual)

    @patch('mpvqc.gui.messageboxes.mb_boxes.UnsavedChangesQuitMessageBox')
    def test_unsaved_changes_quit_popup(self, mocked_box: Mock, *_):
        MessageBoxes.unsaved_changes_quit()
        mocked_box.return_value.popup.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_boxes.UnsavedChangesQuitMessageBox')
    def test_unsaved_changes_quit_response(self, mocked_box: Mock, *_):
        expected = UnsavedChangesQuitResponse.QUIT
        mocked_box.return_value.response.return_value = expected
        actual = MessageBoxes.unsaved_changes_quit()

        self.assertEqual(expected, actual)

    @patch('mpvqc.gui.messageboxes.mb_boxes.ValidVideoFileFoundMessageBox')
    def test_valid_video_found_popup(self, mocked_box: Mock, *_):
        MessageBoxes.valid_video_found()
        mocked_box.return_value.popup.assert_called()

    @patch('mpvqc.gui.messageboxes.mb_boxes.ValidVideoFileFoundMessageBox')
    def test_valid_video_found_response(self, mocked_box: Mock, *_):
        expected = ValidVideoFileFoundResponse.OPEN
        mocked_box.return_value.response.return_value = expected
        actual = MessageBoxes.valid_video_found()

        self.assertEqual(expected, actual)
