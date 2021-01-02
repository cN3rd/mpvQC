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

from mpvqc.engine.handler.flow_handler import ModifyCommentsFlowHandler
from mpvqc.engine.interface import Options
from test.engine import PlayerTestImpl, AppTestImpl, TableTestImpl


class Test(unittest.TestCase):
    FLOW_ACTIONS = 'mpvqc.engine.handler.flow_handler.modify_comments.ModifyCommentsFlowActions'

    OPTIONS = Options(
        AppTestImpl(),
        PlayerTestImpl(),
        TableTestImpl()
    )

    @patch(f'{FLOW_ACTIONS}.modified_comments')
    def test_modify(self, mocked_modify: Mock):
        handler = ModifyCommentsFlowHandler()
        handler.handle_flow_with(self.OPTIONS)
        mocked_modify.assert_called()

    def test_modify_changes_registered(self):
        handler = ModifyCommentsFlowHandler()
        self.assertFalse(handler.get_changes().changed_comments)
        handler.handle_flow_with(self.OPTIONS)
        self.assertTrue(handler.get_changes().changed_comments)
