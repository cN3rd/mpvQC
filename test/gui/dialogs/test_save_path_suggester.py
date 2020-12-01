import unittest
from pathlib import Path

from mpvqc.gui.dialogs.save_path_suggester import SavePathSuggester


class TestSavePathSuggester(unittest.TestCase):
    PATH_ANY = Path() / 'does' / 'not' / 'exist.mkv'
    PATH_HOME = Path.home()

    def test_video_nick(self):
        video = self.PATH_ANY
        nick = 'mpvqc'

        expected = Path() / 'does' / 'not' / '[QC]_exist_mpvqc.txt'
        actual = SavePathSuggester.suggest(video, nick)

        self.assertEqual(expected, actual)

    def test_video(self):
        video = self.PATH_ANY
        nick = None

        expected = Path() / 'does' / 'not' / '[QC]_exist.txt'
        actual = SavePathSuggester.suggest(video, nick)

        self.assertEqual(expected, actual)

    def test_nick(self):
        video = None
        nick = 'mpvqc'

        expected = Path().home() / '[QC]_untitled_mpvqc.txt'
        actual = SavePathSuggester.suggest(video, nick)

        self.assertEqual(expected, actual)

    def test_no(self):
        video = None
        nick = None

        expected = Path().home() / '[QC]_untitled.txt'
        actual = SavePathSuggester.suggest(video, nick)

        self.assertEqual(expected, actual)
