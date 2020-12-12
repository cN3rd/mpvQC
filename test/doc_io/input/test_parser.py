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
from typing import Optional, Tuple

from mpvqc.doc_io.input.parser import DocumentLineParser
from mpvqc.engine.comment import Comment
from test.doc_io.input import ANY_VIDEO


class TestDocumentLineParser(unittest.TestCase):

    def _test_comment(self, expected: Optional[Comment], line: str):
        parser = DocumentLineParser()
        parser.parse(line)

        comments = parser.get_comments()

        expected = expected
        actual = comments[0] if comments else None

        self.assertEqual(expected, actual)

    def _test_comments(self, expected: Tuple[Comment], *lines: str):
        parser = DocumentLineParser()
        for line in lines:
            parser.parse(line)

        expected = expected
        actual = parser.get_comments()

        self.assertEqual(expected, actual)

    def _test_videos(self, expected: Optional[Path], *lines: str):
        parser = DocumentLineParser()
        for line in lines:
            parser.parse(line)

        video = parser.get_video()

        expected = expected.resolve() if expected else None
        actual = video.resolve() if video else None

        self.assertEqual(expected, actual)

    def test_video_unavailable(self):
        video = ''
        line = f'path : {video}'
        expected = None
        self._test_videos(expected, line)

    def test_video_normally(self):
        video = ANY_VIDEO
        line = f'path : {video}'
        expected = video.resolve()
        self._test_videos(expected, line)

    def test_video_with_newline_at_the_end(self):
        video = ANY_VIDEO
        line = f'path : {video}\n'
        expected = video.resolve()
        self._test_videos(expected, line)

    def test_video_without_space_between(self):
        video = ANY_VIDEO
        line = f'path:{video}'
        expected = video.resolve()
        self._test_videos(expected, line)

    def test_video_with_space_before_colon(self):
        video = ANY_VIDEO
        line = f'path :{video}'
        expected = video.resolve()
        self._test_videos(expected, line)

    def test_video_with_space_after_colon(self):
        video = ANY_VIDEO
        line = f'path: {video}'
        expected = video.resolve()
        self._test_videos(expected, line)

    def test_video_first_one_wins(self):
        video1 = ANY_VIDEO
        video2 = ANY_VIDEO
        line1 = f'path: {video1}'
        line2 = f'path: {video2}'
        expected = video1.resolve()
        self._test_videos(expected, line1, line2)

    def test_comment_unavailable(self):
        line = f''
        expected = None
        self._test_comment(expected, line)

    def test_comment_normally(self):
        time, category, note = '00:00:00', 'Translation', 'this is a note'
        line = f'[{time}] [{category}] {note}'
        expected = Comment(time, category, note)
        self._test_comment(expected, line)

    def test_comment_with_newline_at_the_end(self):
        time, category, note = '00:00:00', 'Translation', 'this is a note'
        line = f'[{time}] [{category}] {note}\n'
        expected = Comment(time, category, note)
        self._test_comment(expected, line)

    def test_comment_without_space_between_time_and_category(self):
        time, category, note = '00:00:00', 'Translation', 'this is a note'
        line = f'[{time}][{category}] {note}'
        expected = Comment(time, category, note)
        self._test_comment(expected, line)

    def test_comment_without_space_between_category_and_note(self):
        time, category, note = '00:00:00', 'Translation', 'this is a note'
        line = f'[{time}] [{category}]{note}'
        expected = Comment(time, category, note)
        self._test_comment(expected, line)

    def test_comment_without_space_between(self):
        time, category, note = '00:00:00', 'Translation', 'this is a note'
        line = f'[{time}][{category}]{note}'
        expected = Comment(time, category, note)
        self._test_comment(expected, line)

    def test_comments_collected(self):
        time, category, note = '00:00:00', 'Translation', 'this is a note'
        line1 = f'[{time}][{category}]{note}'
        comment1 = Comment(time, category, note)

        time, category, note = '00:00:01', 'Spelling', 'Good'
        line2 = f'[{time}][{category}]{note}'
        comment2 = Comment(time, category, note)

        expected = tuple([comment1, comment2])
        self._test_comments(expected, line1, line2)