#  mpvQC
#
#  Copyright (C) 2020 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from pathlib import Path

from mpvqc.engine.handler.utility.save_path_suggester import SavePathSuggester


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
