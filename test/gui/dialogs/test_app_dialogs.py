import unittest
from pathlib import Path
from unittest.mock import patch

from mpvqc.gui.dialogs import AppDialogs
from test.gui.dialogs import Mocker


class TestAppDialogs(unittest.TestCase):

    @patch('mpvqc.gui.dialogs.app_dialogs.get_settings', return_value=Mocker('import_last_dir_document', Path('/old')))
    @patch('mpvqc.gui.dialogs.app_dialogs.OpenDocumentsDialog')
    def test_import_document_latest_directory_passed_in(self, mock_dialog, *_):
        AppDialogs.import_documents(parent=None)
        mock_dialog.return_value.open.assert_called_with(Path('/old'))

    @patch('mpvqc.gui.dialogs.app_dialogs.OpenDocumentsDialog')
    @patch('mpvqc.gui.dialogs.app_dialogs.get_settings', return_value=Mocker('import_last_dir_document', Path('/old')))
    def test_import_document_store_latest_existing_directory(self, mock_settings, dialog, *_):
        dialog.return_value.get_documents.return_value = [Path('/new/imported.txt')]
        AppDialogs.import_documents(parent=None)
        self.assertEqual(Path('/new'), mock_settings.return_value.import_last_dir_document)

    @patch('mpvqc.gui.dialogs.app_dialogs.get_settings', return_value=Mocker('import_last_dir_video', Path('/old')))
    @patch('mpvqc.gui.dialogs.app_dialogs.OpenVideoDialog')
    def test_import_video_latest_directory_passed_in(self, mock_dialog, *_):
        AppDialogs.import_video(parent=None)
        mock_dialog.return_value.open.assert_called_with(Path('/old'))

    @patch('mpvqc.gui.dialogs.app_dialogs.OpenVideoDialog')
    @patch('mpvqc.gui.dialogs.app_dialogs.get_settings', return_value=Mocker('import_last_dir_video', Path('/old')))
    def test_import_video_store_latest_existing_directory(self, mock_settings, dialog, *_):
        dialog.return_value.get_video.return_value = Path('/new/imported.mp4')
        AppDialogs.import_video(parent=None)
        self.assertEqual(Path('/new'), mock_settings.return_value.import_last_dir_video)

    @patch('mpvqc.gui.dialogs.app_dialogs.get_settings', return_value=Mocker('import_last_dir_subtitles', Path('/old')))
    @patch('mpvqc.gui.dialogs.app_dialogs.OpenSubtitlesDialog')
    def test_import_subtitles_latest_directory_passed_in(self, mock_dialog, *_):
        AppDialogs.import_subtitles(parent=None)
        mock_dialog.return_value.open.assert_called_with(Path('/old'))

    @patch('mpvqc.gui.dialogs.app_dialogs.OpenSubtitlesDialog')
    @patch('mpvqc.gui.dialogs.app_dialogs.get_settings', return_value=Mocker('import_last_dir_subtitles', Path('/old')))
    def test_import_subtitles_store_latest_existing_directory(self, mock_settings, dialog, *_):
        dialog.return_value.get_subtitles.return_value = [Path('/new/imported.ass')]
        AppDialogs.import_subtitles(parent=None)
        self.assertEqual(Path('/new'), mock_settings.return_value.import_last_dir_subtitles)
