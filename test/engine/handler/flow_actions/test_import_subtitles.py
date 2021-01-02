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
from unittest.mock import patch, Mock

from mpvqc.engine.handler.flow_actions import SubtitleImportFlowActions
from test.doc_io.input import ANY_PATHS
from test.engine import DEFAULT_OPTIONS


class TestSubtitleImportFlowActions(unittest.TestCase):
    GET_SUBTITLES = 'mpvqc.engine.handler.flow_actions.import_subtitles.SubtitleImportDialog.get_subtitles'
    LOAD = 'mpvqc.engine.handler.flow_actions.import_subtitles.SubtitleImporter.load'

    def test_dont_have_subtitles(self):
        we = SubtitleImportFlowActions(DEFAULT_OPTIONS, tuple())
        self.assertFalse(we.have_subtitles())
        self.assertTrue(we.dont_have_subtitles())

    def test_have_subtitles(self):
        we = SubtitleImportFlowActions(DEFAULT_OPTIONS, ANY_PATHS)
        self.assertTrue(we.have_subtitles())
        self.assertFalse(we.dont_have_subtitles())

    @patch(GET_SUBTITLES, return_value=ANY_PATHS)
    def test_ask_for_subtitles(self, *_):
        we = SubtitleImportFlowActions(DEFAULT_OPTIONS, tuple())
        we.ask_via_dialog_for_subtitles()
        self.assertTrue(we.have_subtitles())

    @patch(LOAD)
    def test_load_subtitle(self, mocked_load: Mock):
        we = SubtitleImportFlowActions(DEFAULT_OPTIONS, tuple())
        we.load_subtitles()
        mocked_load.assert_called()
