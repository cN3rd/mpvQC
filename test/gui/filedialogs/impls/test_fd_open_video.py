import unittest
from pathlib import Path
from unittest.mock import patch, ANY, Mock

from mpvqc.gui.filedialogs.impls import OpenVideoDialog


class TestVideoDialog(unittest.TestCase):
    CAPTION = 1
    FILTER = 'filter'

    PATH_ANY = Path() / 'does' / 'not' / 'exist'
    PATH_HOME = Path.home()

    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QWidget')
    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QFileDialog.getOpenFileName')
    def test_open_passed_in_parent(self, mocked_get_open_file_names: Mock, mocked_widget: Mock):
        dialog = OpenVideoDialog(parent=mocked_widget)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(mocked_widget, ANY, ANY, filter=ANY)

    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QFileDialog.getOpenFileName')
    def test_open_passed_in_caption(self, mocked_get_open_file_names: Mock):
        dialog = OpenVideoDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertTrue(mocked_get_open_file_names.call_args_list[0].args[self.CAPTION])

    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QFileDialog.getOpenFileName')
    def test_open_passed_in_directory(self, mocked_get_open_file_names: Mock):
        dialog = OpenVideoDialog(parent=None)
        dialog.open(last_directory=self.PATH_ANY)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_ANY), filter=ANY)

    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QFileDialog.getOpenFileName')
    def test_open_home_by_default(self, mocked_get_open_file_names: Mock):
        dialog = OpenVideoDialog(parent=None)
        dialog.open(last_directory=None)

        mocked_get_open_file_names.assert_called_with(ANY, ANY, str(self.PATH_HOME), filter=ANY)

    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QFileDialog.getOpenFileName')
    def test_open_file_filters_video(self, mocked_get_open_file_names: Mock):
        dialog = OpenVideoDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('*.mp4', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])
        self.assertIn('*.mkv', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])
        self.assertIn('*.avi', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QFileDialog.getOpenFileName')
    def test_open_file_filters_any(self, mocked_get_open_file_names: Mock):
        dialog = OpenVideoDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertIn('(*.*)', mocked_get_open_file_names.call_args_list[0].kwargs[self.FILTER])

    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QFileDialog.getOpenFileName', return_value=('', ''))
    def test_get_video_on_cancel(self, *_):
        dialog = OpenVideoDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertFalse(dialog.get_video())

    @patch('mpvqc.gui.filedialogs.impls.fd_open_video.QFileDialog.getOpenFileName', return_value=(['/home/mpvqc/yep.mp4'], ''))
    def test_get_video_on_success(self, *_):
        dialog = OpenVideoDialog(parent=None)
        dialog.open(last_directory=None)

        self.assertEqual(dialog.get_video().resolve(), Path('/home/mpvqc/yep.mp4').resolve())
