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
    def test_open_passed_in_parent(self, mocked_get_open_file_names, mocked_widget):
        dialog = OpenDocumentsDialog(parent=mocked_widget)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(mocked_widget, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_passed_in_caption(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(mocked_get_open_file_names.call_args_list[0].args[self.CAPTION])

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_passed_in_path(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=self.PATH_ANY)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_ANY), filter=ANY)

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_directory_home_by_default(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_HOME), filter=ANY)

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_file_filters_txt(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('(*.txt)', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames')
    def test_open_file_filters_any(self, mocked_get_open_file_names):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('(*.*)', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames', return_value=([], ''))
    def test_get_documents_on_cancel(self, *_):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertFalse(dialog.get_documents())

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames', return_value=(['/home/mpvqc/yep.txt'], ''))
    def test_get_documents_on_1_import(self, *_):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertEqual(1, len(dialog.get_documents()))

    @patch('mpvqc.gui.dialogs.open_documents.QFileDialog.getOpenFileNames', return_value=(['/home', '/another-home'], ''))
    def test_get_documents_on_x_import(self, *_):
        dialog = OpenDocumentsDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(len(dialog.get_documents()) > 1)
