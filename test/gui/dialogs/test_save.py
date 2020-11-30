import unittest
from pathlib import Path
from unittest.mock import patch, ANY

from mpvqc.gui.dialogs.save import SaveDialog


class TestSave(unittest.TestCase):
    CAPTION = 1
    PATH = 2
    FILTER = 'filter'

    PATH_ANY = Path() / 'does' / 'not' / 'exist.mkv'
    PATH_HOME = Path.home()

    @patch('mpvqc.gui.dialogs.save.QWidget')
    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_existing_parent_is_passed_in(self, mocked_get_save_file_name, mocked_widget):
        dialog = SaveDialog(parent=mocked_widget)
        dialog.open(None)

        mocked_get_save_file_name.assert_called_with(mocked_widget, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_non_existing_parent_is_passed_in(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(None)

        mocked_get_save_file_name.assert_called_with(None, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_caption_exists(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(None)

        self.assertTrue(mocked_get_save_file_name.call_args[self.CAPTION])

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_directory_home_by_default(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(None)

        arg_path = mocked_get_save_file_name.call_args_list[0].args[self.PATH]
        self.assertTrue(arg_path.startswith(str(self.PATH_HOME)))

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_directory_passed_in(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(at=self.PATH_ANY)

        arg_path = mocked_get_save_file_name.call_args_list[0].args[self.PATH]
        self.assertTrue(arg_path.startswith(str(self.PATH_ANY.parent)))

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_allowed_file_filters_txt(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(None)

        self.assertIn('(*.txt)', mocked_get_save_file_name.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_allowed_file_filters_any(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(None)

        self.assertIn('(*.*)', mocked_get_save_file_name.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName', return_value=('', ''))
    def test_get_location_returns_none_if_user_cancels_export(self, *_):
        dialog = SaveDialog(parent=None)
        dialog.open(None)

        self.assertFalse(dialog.get_location())

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName', return_value=('/home/mpvqc/yep.txt', ''))
    def test_get_documents_returns_location_on_default_case(self, *_):
        dialog = SaveDialog(parent=None)
        dialog.open(None)

        self.assertEqual(dialog.get_location().resolve(), Path('/home/mpvqc/yep.txt').resolve())
