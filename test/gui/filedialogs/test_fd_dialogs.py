import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from mpvqc.gui.filedialogs import Dialogs
from test.gui.filedialogs import Mocker


class TestAppDialogs(unittest.TestCase):

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_document', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenDocumentsDialog')
    def test_import_document_latest_directory_passed_in(self, mock_dialog: Mock, *_):
        Dialogs.import_documents(parent=None)
        mock_dialog.return_value.open.assert_called_with(Path('/old'))

    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenDocumentsDialog')
    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_document', Path('/old')))
    def test_import_document_store_latest_existing_directory(self, mock_settings: Mock, dialog: Mock, *_):
        dialog.return_value.get_documents.return_value = [Path('/new/imported.txt')]
        Dialogs.import_documents(parent=None)
        self.assertEqual(Path('/new'), mock_settings.return_value.import_last_dir_document)

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_document', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenDocumentsDialog')
    def test_import_document_returns_documents_on_success(self, dialog: Mock, *_):
        documents_user = tuple([Path('/new/imported.txt'), Path('/new/imported2.txt')])
        dialog.return_value.get_documents.return_value = documents_user
        documents_returned = Dialogs.import_documents(parent=None)
        self.assertEqual(documents_user, documents_returned)

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_document', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenDocumentsDialog')
    def test_import_document_returns_documents_on_cancel(self, dialog: Mock, *_):
        documents_user = tuple([])
        dialog.return_value.get_documents.return_value = documents_user
        documents_returned = Dialogs.import_documents(parent=None)
        self.assertEqual(documents_user, documents_returned)

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_video', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenVideoDialog')
    def test_import_video_latest_directory_passed_in(self, mock_dialog: Mock, *_):
        Dialogs.import_video(parent=None)
        mock_dialog.return_value.open.assert_called_with(Path('/old'))

    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenVideoDialog')
    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_video', Path('/old')))
    def test_import_video_store_latest_existing_directory(self, mock_settings: Mock, dialog: Mock, *_):
        dialog.return_value.get_video.return_value = Path('/new/imported.mp4')
        Dialogs.import_video(parent=None)
        self.assertEqual(Path('/new'), mock_settings.return_value.import_last_dir_video)

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_video', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenVideoDialog')
    def test_import_video_returns_video_on_success(self, dialog: Mock, *_):
        video_user = Path('/new/imported.mp4')
        dialog.return_value.get_video.return_value = video_user
        video_returned = Dialogs.import_video(parent=None)
        self.assertEqual(video_user, video_returned)

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_video', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenVideoDialog')
    def test_import_video_returns_video_on_cancel(self, dialog: Mock, *_):
        video_user = None
        dialog.return_value.get_video.return_value = video_user
        video_returned = Dialogs.import_video(parent=None)
        self.assertEqual(video_user, video_returned)

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_subtitles', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenSubtitlesDialog')
    def test_import_subtitles_latest_directory_passed_in(self, mock_dialog: Mock, *_):
        Dialogs.import_subtitles(parent=None)
        mock_dialog.return_value.open.assert_called_with(Path('/old'))

    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenSubtitlesDialog')
    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_subtitles', Path('/old')))
    def test_import_subtitles_store_latest_existing_directory(self, mock_settings: Mock, dialog: Mock, *_):
        dialog.return_value.get_subtitles.return_value = [Path('/new/imported.ass')]
        Dialogs.import_subtitles(parent=None)
        self.assertEqual(Path('/new'), mock_settings.return_value.import_last_dir_subtitles)

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_subtitles', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenSubtitlesDialog')
    def test_import_subtitles_returns_subtitles_on_success(self, dialog: Mock, *_):
        subtitles_user = tuple([Path('/new/imported.ass'), Path('/new/imported2.ass')])
        dialog.return_value.get_subtitles.return_value = subtitles_user
        subtitles_returned = Dialogs.import_subtitles(parent=None)
        self.assertEqual(subtitles_user, subtitles_returned)

    @patch('mpvqc.gui.filedialogs.fd_dialogs.get_settings', return_value=Mocker('import_last_dir_subtitles', Path('/old')))
    @patch('mpvqc.gui.filedialogs.fd_dialogs.OpenSubtitlesDialog')
    def test_import_subtitles_returns_subtitles_on_cancel(self, dialog: Mock, *_):
        subtitles_user = tuple([])
        dialog.return_value.get_subtitles.return_value = subtitles_user
        subtitles_returned = Dialogs.import_subtitles(parent=None)
        self.assertEqual(subtitles_user, subtitles_returned)
