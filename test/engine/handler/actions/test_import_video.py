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

from mpvqc.engine.handler.actions import VideoImporter
from test.doc_io.input import ANY_PATH

from test.engine import PlayerTestImpl


class TestVideoImporter(unittest.TestCase):

    def test_import_subtitle_import(self):
        player = PlayerTestImpl()
        video = ANY_PATH

        importer = VideoImporter(player=player)
        importer.load(video=video)

        self.assertTrue(player.open_called)
        self.assertEqual(video, player._open_video_args)
