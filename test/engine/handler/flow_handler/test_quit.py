#  mpvQC
#
#  Copyright (C) 2021 mpvQC developers
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

from mpvqc.engine.handler.flow_handler import QuitQuestionFlowHandler
from test.engine import DEFAULT_OPTIONS


class Test(unittest.TestCase):
    FLOW_ACTIONS = 'mpvqc.engine.handler.flow_handler.quit.QuitFlowQuestion'

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=True)
    @patch(f'{FLOW_ACTIONS}.ask_via_message_box_to_quit')
    def test_ask_to_quit_true(self, mocked_ask: Mock, *_):
        handler = QuitQuestionFlowHandler(have_unsaved_changes=True)
        handler.ask_with(DEFAULT_OPTIONS)
        mocked_ask.assert_called()

    @patch(f'{FLOW_ACTIONS}.have_unsaved_changes', return_value=False)
    @patch(f'{FLOW_ACTIONS}.ask_via_message_box_to_quit')
    def test_ask_to_quit_false(self, mocked_ask: Mock, *_):
        handler = QuitQuestionFlowHandler(have_unsaved_changes=True)
        handler.ask_with(DEFAULT_OPTIONS)
        mocked_ask.assert_not_called()
