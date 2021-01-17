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

from mpvqc.core import Comment
from mpvqc.core.engine.handler.actions import CommentsImporter

from test.core.engine import TableTestImpl


class TestCommentsImporter(unittest.TestCase):

    def test_import_comments(self):
        table = TableTestImpl()

        comments = tuple([
            Comment(time='00:00:00', category='Test', comment='Test 1'),
            Comment(time='00:00:00', category='Test-2', comment='Test 2'),
            Comment(time='00:00:00', category='Test', comment='Test 2'),
        ])

        importer = CommentsImporter(table=table)
        importer.load(comments)

        self.assertTrue(table.add_called)
        self.assertEqual(comments, table.add_arguments)
