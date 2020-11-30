import unittest
from pathlib import Path
from unittest.mock import patch, ANY

from mpvqc.gui.dialogs import OpenDocumentsDialog


class TestDocumentsDialog(unittest.TestCase):
    CAPTION = 1
    FILTER = 'filter'

    PATH_ANY = Path() / 'does' / 'not' / 'exist'
    PATH_HOME = Path.home()

    @patch('mpvqc.gui.dialogs.open_documents.QWidget')
    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_existing_parent_is_passed_in(self, mocked_get_open_file_names, mocked_widget):
        dialog = OpenDocumentsDialog(parent=mocked_widget)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(mocked_widget, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_non_existing_parent_is_passed_in(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(None, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_caption_exists(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(mocked_get_open_file_names.call_args_list[0].args[self.CAPTION])

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_directory_home_by_default(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_HOME), filter=ANY)

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_directory_passed_in(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=self.PATH_ANY)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_ANY), filter=ANY)

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_allowed_file_filters_txt(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('(*.txt)', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_allowed_file_filters_any(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('(*.*)', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames', return_value=([], ''))
    def test_get_documents_returns_none_if_user_cancels_import(self, *_):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertFalse(dialog.get_documents())

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames', return_value=(['/home/mpvqc/yep.txt'], ''))
    def test_get_documents_returns_one_document_on_one_document_import(self, *_):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertEqual(1, len(dialog.get_documents()))

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames', return_value=(['/home', '/another-home'], ''))
    def test_get_documents_returns_multiple_documents_on_multiple_document_import(self, *_):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(len(dialog.get_documents()) > 1)
