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
from typing import Tuple
from unittest.mock import patch, mock_open

from mpvqc.doc_io import Document
from mpvqc.doc_io.input.error import NotADocumentError
from mpvqc.doc_io.input.reader import FileReader
from test.doc_io.input import ANY_PATH


class TestFileReader(unittest.TestCase):
    PATH = ANY_PATH

    def _full_example(self) -> Tuple[Document, Path, str]:
        path = self.PATH / "video gets parsed.mp4"

        time, category, note = '00:00:00', 'Translation', 'this is a note'
        comment = f'[{time}] [{category}]{note}'

        content = f'[FILE]\n' \
                  f'path : {path}\n' \
                  f'\n' \
                  f'{comment}\n' \
                  f'{comment}\n'

        return self._read(content), path, note

    def _read(self, feed: str) -> Document:
        with patch('pathlib.Path.open', mock_open(read_data=feed)):
            with self.PATH.open():
                reader = FileReader(self.PATH)
                reader.read()
                return reader.get_document()

    def test_file_incompatible_empty(self):
        content = ''

        self.assertRaises(NotADocumentError, self._read, content)

    def test_file_incompatible(self):
        content = f'[NOT A FILE]'

        self.assertRaises(NotADocumentError, self._read, content)

    def test_file_compatible(self):
        content = f'[FILE]'
        try:
            self._read(content)
        except NotADocumentError:
            self.fail(f'A file starting with {content} is a valid file')

    def test_file_not_none(self):
        content = f'[FILE]'
        document = self._read(content)
        self.assertIsNotNone(document.file)

    def test_comment_always_tuple(self):
        content = f'[FILE]'
        document = self._read(content)
        self.assertTrue(isinstance(document.comments, tuple))

    def test_video_parsed(self):
        path = self.PATH / "video gets parsed.mp4"
        content = f'[FILE]\n' \
                  f'path : {path}\n'
        document = self._read(content)

        self.assertIsNotNone(document.video)
        self.assertEqual(path.resolve(), document.video.resolve())

    def test_comment_parsed(self):
        time, category, note = '00:00:00', 'Translation', 'this is a note'
        comment = f'[{time}] [{category}]{note}'
        content = f'[FILE]\n' \
                  f'{comment}\n'

        document = self._read(content)
        comments = document.comments

        self.assertTrue(comments)

    def test_comment_parsed_multiple(self):
        time, category, note = '00:00:00', 'Translation', 'this is a note'
        comment = f'[{time}] [{category}]{note}'
        content = f'[FILE]\n' \
                  f'{comment}\n' \
                  f'{comment}\n'

        document = self._read(content)
        comments = document.comments

        self.assertTrue(len(comments) == 2)

    def test_full_file_video_parsed(self):
        document, path, _ = self._full_example()
        video = document.video

        self.assertIsNotNone(video)
        self.assertEqual(path.resolve(), video.resolve())

    def test_full_file_comment_parsed(self):
        document, _, note = self._full_example()
        comments = document.comments

        comment = comments[0]

        self.assertEqual(note, comment.comment_note)
