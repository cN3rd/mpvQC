# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re
from pathlib import Path
from typing import List

from mpvqc.manager_new.comment import Comment
from mpvqc.manager_new.document import Document

INVALID = Document(video=Path(''), comments=tuple())


class DocumentParser:
    VIDEO = re.compile(r'^path\s*:\s*(?P<path>.+)\s*')

    _TIME = r'\[(?P<time>\d{2}:\d{2}:\d{2})]'
    _TYPE = r'\[(?P<type>[^\[\]]+)]'
    _NOTE = r'(?P<comment>.*)'
    COMMENT = re.compile(f'{_TIME}\\s*{_TYPE}\\s*{_NOTE}\\s*')

    def __init__(self):
        self._video = ''
        self._comments: List[Comment] = []

    def parse(self, line: str):
        if not self._video:
            self._parse_video(line)
            if self._video:
                return

        self._parse_comment(line)

    def _parse_video(self, line: str):
        match = self.VIDEO.match(line)
        if match is None:
            return

        self._video = match.group('path').strip()

    def _parse_comment(self, line: str):
        match = self.COMMENT.match(line)
        if match is None:
            return

        comment = Comment(
            time=match.group('time'),
            category=match.group('type'),
            comment=match.group('comment').strip()
        )
        self._comments.append(comment)

    def get_document(self) -> Document:
        return Document(video=Path(self._video), comments=tuple(self._comments))


class Importer:
    PREFIX = '[FILE]'

    def import_this(self, file: Path) -> Document:
        lines = self._read(file)
        first_line = self._first_line_from(lines)

        if self._is_valid(first_line):
            return self._parse(lines)
        else:
            return INVALID

    @staticmethod
    def _read(file: Path):
        with file.open('r', encoding='utf-8-sig') as f:
            return f.read().splitlines()

    @staticmethod
    def _first_line_from(lines: List[str]) -> str:
        return lines[0] if lines else ''

    def _is_valid(self, first_line: str):
        return first_line.startswith(self.PREFIX)

    @staticmethod
    def _parse(lines: List[str]) -> Document:
        parser = DocumentParser()
        for line in lines:
            parser.parse(line)

        return parser.get_document()
