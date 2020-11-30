import unittest
from pathlib import Path
from unittest.mock import patch, ANY

from mpvqc.gui.dialogs import OpenSubtitlesDialog


class TestDocumentsDialog(unittest.TestCase):
    CAPTION = 1
    FILTER = 'filter'

    PATH_ANY = Path() / 'does' / 'not' / 'exist'
    PATH_HOME = Path.home()

    @patch('mpvqc.gui.dialogs.open_subtitles.QWidget')
    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_existing_parent_is_passed_in(self, mocked_get_open_file_names, mocked_widget):
        dialog = OpenSubtitlesDialog(parent=mocked_widget)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(mocked_widget, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_non_existing_parent_is_passed_in(self, mocked_get_open_file_names):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(None, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_caption_exists(self, mocked_get_open_file_names):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(mocked_get_open_file_names.call_args_list[0].args[self.CAPTION])

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_directory_home_by_default(self, mocked_get_open_file_names):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_HOME), filter=ANY)

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_directory_passed_in(self, mocked_get_open_file_names):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=self.PATH_ANY)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_ANY), filter=ANY)

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_allowed_file_filters(self, mocked_get_open_file_names):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('*.ass', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])
        self.assertIn('*.ssa', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])
        self.assertIn('*.srt', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames')
    def test_open_allowed_file_filters_any(self, mocked_get_open_file_names):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('(*.*)', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames', return_value=([], ''))
    def test_get_subtitles_returns_none_if_user_cancels_import(self, *_):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertFalse(dialog.get_subtitles())

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames', return_value=(['/home/mpvqc/yep.txt'], ''))
    def test_get_subtitles_returns_one_subtitle_on_one_subtitle_import(self, *_):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertEqual(1, len(dialog.get_subtitles()))

    @patch('mpvqc.gui.dialogs.open_subtitles.QFileDialog.getOpenFileNames', return_value=(['/home', '/another-home'], ''))
    def test_get_subtitle_returns_multiple_subtitles_on_multiple_subtitle_import(self, *_):
        dialog = OpenSubtitlesDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(len(dialog.get_subtitles()) > 1)
