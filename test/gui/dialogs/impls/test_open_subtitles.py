import unittest
from pathlib import Path
from unittest.mock import patch, ANY, Mock

from mpvqc.gui.dialogs.impls import OpenSubtitlesDialog


class TestSubtitlesDialog(unittest.TestCase):
    CAPTION = 1
    FILTER = 'filter'

    PATH_ANY = Path() / 'does' / 'not' / 'exist'
    PATH_HOME = Path.home()

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QWidget')
    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_passed_in_parent(self, mocked_get_open_file_names: Mock, mocked_widget: Mock):
        dialog = OpenSubtitlesDialog(parent=mocked_widget)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(mocked_widget, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_passed_in_caption(self, mocked_get_open_file_names: Mock):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(mocked_get_open_file_names.call_args_list[0].args[self.CAPTION])

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_passed_in_path(self, mocked_get_open_file_names: Mock):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=self.PATH_ANY)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_ANY), filter=ANY)

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_home_by_default(self, mocked_get_open_file_names: Mock):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_HOME), filter=ANY)

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_file_filters_subs(self, mocked_get_open_file_names: Mock):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('*.ass', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])
        self.assertIn('*.ssa', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])
        self.assertIn('*.srt', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_file_filters_any(self, mocked_get_open_file_names: Mock):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('(*.*)', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames', return_value=([], ''))
    def test_get_subtitles_on_cancel(self, *_):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertFalse(dialog.get_subtitles())

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames', return_value=(['/home/mpvqc/yep.txt'], ''))
    def test_get_subtitles_on_1_import(self, *_):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertEqual(1, len(dialog.get_subtitles()))

    @patch('mpvqc.gui.dialogs.impls.open_subtitles.QFileDialog.getOpenFileNames', return_value=(['/home', '/another-home'], ''))
    def test_get_subtitles_on_x_import(self, *_):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(len(dialog.get_subtitles()) > 1)
