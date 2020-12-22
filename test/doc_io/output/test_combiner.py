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

from mpvqc.doc_io.output.combiner import DocumentCombiner
from mpvqc.core import Comment


class TestDocumentCombiner(unittest.TestCase):

    def test_empty(self):
        doc = DocumentCombiner()
        self.assertFalse(doc.combine())

    def test_file_tag(self):
        doc = DocumentCombiner()
        doc.write_file_tag()
        self.assertEqual('[FILE]', doc.combine())

    def test_write_single_date(self):
        doc = DocumentCombiner()
        doc.write_file_tag()
        doc.write_date('now')

        lines = doc.combine().splitlines(keepends=False)

        self.assertIn('now', lines[1])

    def test_write_single_generator(self):
        doc = DocumentCombiner()
        doc.write_file_tag()
        doc.write_generator('iGenerator')

        lines = doc.combine().splitlines(keepends=False)

        self.assertIn('iGenerator', lines[1])

    def test_write_single_nick(self):
        doc = DocumentCombiner()
        doc.write_file_tag()
        doc.write_nick('best-test')

        lines = doc.combine().splitlines(keepends=False)

        self.assertIn('best-test', lines[1])

    def test_write_single_path(self):
        path = Path()

        doc = DocumentCombiner()
        doc.write_file_tag()
        doc.write_path(path)

        lines = doc.combine().splitlines(keepends=False)

        self.assertIn(str(path), lines[1])

    def test_write_full_header(self):
        path = Path()

        doc = DocumentCombiner()
        doc.write_file_tag()
        doc.write_date('now')
        doc.write_generator('iGenerator')
        doc.write_nick('best-test')
        doc.write_path(path)

        lines = doc.combine().splitlines(keepends=False)

        self.assertTrue(len(lines) == 5)

    def test_write_two_empty_lines(self):
        doc = DocumentCombiner()
        doc.write_file_tag()
        doc.write_empty_line()
        doc.write_empty_line()
        doc.write_data_tag()
        doc = doc.combine()

        lines = doc.splitlines(keepends=False)
        self.assertEqual(2, len([line for line in lines if not line]), 'Document should contain 2 empty lines')

    def test_write_comment(self):
        comments = [
            Comment(time="00:00:00", category="pestilential", comment="please no!"),
            Comment(time="10:00:00", category="covid", comment="please not again!"),
        ]
        doc = DocumentCombiner()
        doc.write_data_tag()
        doc.write_comments(tuple(comments))
        doc = doc.combine()

        for comment in comments:
            self.assertIn(str(comment), doc)

    def test_write_comment_amount(self):
        comments = [
            Comment(time="00:00:00", category="pestilential", comment="please no!"),
            Comment(time="00:00:07", category="covid", comment="please not again!"),
            Comment(time="00:00:00", category="no words", comment=""),
        ]
        doc = DocumentCombiner()
        doc.write_comments(tuple(comments))
        doc.write_comment_summary()
        doc = doc.combine()

        line_summary = doc.splitlines(keepends=False)[-1]
        self.assertTrue(line_summary.split()[-1].isdigit(), 'Comment amount is missing')
        self.assertTrue(line_summary.endswith(f'{len(comments)}'), 'Comment amount is wrong')
