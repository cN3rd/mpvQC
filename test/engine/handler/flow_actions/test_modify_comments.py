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

from mpvqc.engine.handler.flow_actions import ModifyCommentsFlowActions


class TestSubtitleImportFlowActions(unittest.TestCase):

    def test_no_modified_comments(self):
        we = ModifyCommentsFlowActions()
        self.assertFalse(we.get_changes().changed_comments)

    def test_modified_comments(self):
        we = ModifyCommentsFlowActions()
        we.modified_comments()
        self.assertTrue(we.get_changes().changed_comments)
