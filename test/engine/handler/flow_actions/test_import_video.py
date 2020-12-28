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

from mpvqc.engine.handler.flow_actions import VideoImportFlowActions
from mpvqc.engine.interface import Options
from test.doc_io.input import ANY_VIDEO
from test.engine import PlayerTestImpl, AppTestImpl, TableTestImpl


class TestSubtitleImportFlowActions(unittest.TestCase):
    GET_VIDEO = 'mpvqc.engine.handler.flow_actions.import_video.VideoImportDialog.get_video'
    PATH_IS_FILE = 'mpvqc.engine.handler.flow_actions.import_video.Path.is_file'

    MB_FOUND_VIDEO_ASK = 'mpvqc.engine.handler.flow_actions.import_video.VideoFoundMessageBox.ask'
    MB_FOUND_VIDEO_OPEN = 'mpvqc.engine.handler.flow_actions.import_video.VideoFoundMessageBox.do_we_open'

    LOAD = 'mpvqc.engine.handler.flow_actions.import_video.VideoImporter.load'

    OPTIONS = Options(
        AppTestImpl(),
        PlayerTestImpl(),
        TableTestImpl()
    )

    def test_dont_have_video(self):
        we = VideoImportFlowActions(self.OPTIONS, video_path=None)
        self.assertFalse(we.have_video())
        self.assertTrue(we.dont_have_a_video())

    def test_have_video(self):
        we = VideoImportFlowActions(self.OPTIONS, video_path=ANY_VIDEO)
        self.assertTrue(we.have_video())
        self.assertFalse(we.dont_have_a_video())

    @patch(GET_VIDEO, return_value=ANY_VIDEO)
    def test_ask_for_video(self, *_):
        we = VideoImportFlowActions(self.OPTIONS, video_path=None)
        we.ask_via_dialog_for_video()
        self.assertTrue(we.have_video())

    def test_video_doesnt_exist_no_video(self):
        we = VideoImportFlowActions(self.OPTIONS, video_path=None)
        self.assertFalse(we.confirm_the_video_exists())

    def test_video_doesnt_exist_no_valid_video(self):
        we = VideoImportFlowActions(self.OPTIONS, video_path=ANY_VIDEO)
        self.assertFalse(we.confirm_the_video_exists())

    @patch(PATH_IS_FILE, return_value=True)
    def test_video_exists(self, *_):
        we = VideoImportFlowActions(self.OPTIONS, video_path=ANY_VIDEO)
        self.assertTrue(we.confirm_the_video_exists())

    def test_video_not_playing(self):
        we = VideoImportFlowActions(self.OPTIONS, video_path=None)
        self.assertTrue(we.see_the_video_is_not_already_playing())

    def test_video_is_playing(self):
        options = Options(
            AppTestImpl(),
            PlayerTestImpl(has_video=True, video=ANY_VIDEO),
            TableTestImpl()
        )
        we = VideoImportFlowActions(options, video_path=ANY_VIDEO)
        self.assertFalse(we.see_the_video_is_not_already_playing())

    @patch(MB_FOUND_VIDEO_ASK)
    def test_want_to_open_found_video_ask(self, mocked_ask: Mock):
        we = VideoImportFlowActions(self.OPTIONS, video_path=None)
        we.ask_via_message_box_to_open_found_video()
        mocked_ask.assert_called()

    @patch(MB_FOUND_VIDEO_OPEN)
    def test_want_to_open_found_video_open(self, mocked_ask: Mock):
        we = VideoImportFlowActions(self.OPTIONS, video_path=None)
        we.want_to_open_found_video()
        mocked_ask.assert_called()

    @patch(LOAD)
    def test_load_video_called(self, mocked_load: Mock):
        we = VideoImportFlowActions(self.OPTIONS, video_path=ANY_VIDEO)
        we.load_video()
        mocked_load.assert_called()

    @patch(LOAD)
    def test_load_video_changes_registered(self, *_):
        we = VideoImportFlowActions(self.OPTIONS, video_path=ANY_VIDEO)
        self.assertFalse(we.get_changes().loaded_video)
        we.load_video()
        self.assertTrue(we.get_changes().loaded_video)
