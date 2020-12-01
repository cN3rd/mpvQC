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
    def test_open_passed_in_parent(self, mocked_get_save_file_name, mocked_widget):
        dialog = SaveDialog(parent=mocked_widget)
        dialog.open(at=self.PATH_ANY)

        mocked_get_save_file_name.assert_called_with(mocked_widget, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_passed_in_caption(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(at=self.PATH_ANY)

        self.assertTrue(mocked_get_save_file_name.call_args[self.CAPTION])

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_passed_in_path(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(at=self.PATH_ANY)

        arg_path = mocked_get_save_file_name.call_args_list[0].args[self.PATH]
        self.assertEqual(Path(arg_path).resolve(), self.PATH_ANY.resolve())

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_file_filters_txt(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(at=self.PATH_ANY)

        self.assertIn('(*.txt)', mocked_get_save_file_name.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName')
    def test_open_file_filters_any(self, mocked_get_save_file_name):
        dialog = SaveDialog(parent=None)
        dialog.open(at=self.PATH_ANY)

        self.assertIn('(*.*)', mocked_get_save_file_name.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName', return_value=('', ''))
    def test_get_location_on_cancel(self, *_):
        dialog = SaveDialog(parent=None)
        dialog.open(at=self.PATH_ANY)

        self.assertFalse(dialog.get_location())

    @patch('mpvqc.gui.dialogs.save.QFileDialog.getSaveFileName', return_value=('/home/mpvqc/yep.txt', ''))
    def test_get_location_on_success(self, *_):
        dialog = SaveDialog(parent=None)
        dialog.open(at=self.PATH_ANY)

        self.assertEqual(dialog.get_location().resolve(), Path('/home/mpvqc/yep.txt').resolve())
