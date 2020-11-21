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
from typing import NamedTuple, Optional, Tuple, List

from mpvqc.manager_new._comment import Comment


class Import(NamedTuple):
    video: Optional[Path]
    comments: Tuple[Comment]


INVALID = Import(video=Path(''), comments=tuple())


class Importer:
    PREFIX = '[FILE]'

    VIDEO = re.compile(r'^path\s*:\s*(?P<path>.+)\s*')

    _TIME = r'\[(?P<time>\d{2}:\d{2}:\d{2})]'
    _TYPE = r'\[(?P<type>[^\[\]]+)]'
    _NOTE = r'(?P<comment>.*)'
    COMMENT = re.compile(f"{_TIME}\\s*{_TYPE}\\s*{_NOTE}\\s*")

    def import_this(self, file: Path) -> Import:
        lines = self._read(file)
        first_line = self._first_line_from(lines)

        if self._is_valid(first_line):
            return self._now_parse_all(lines)
        else:
            return INVALID

    @staticmethod
    def _read(file: Path):
        with file.open("r", encoding="utf-8-sig") as f:
            return f.read().splitlines()

    @staticmethod
    def _first_line_from(lines: List[str]) -> str:
        return lines[0] if lines else ""

    def _is_valid(self, first_line: str):
        return first_line.startswith(self.PREFIX)

    def _now_parse_all(self, lines: List[str]) -> Import:
        video, comments = '', []
        for line in lines:
            if not video:
                video = self._parse_video(line)
                if video:
                    continue

            comment = self._parse_comment(line)
            if comment:
                comments.append(comment)

        return Import(video=Path(video), comments=tuple(comments))

    def _parse_video(self, line: str) -> str:
        match = self.VIDEO.match(line)
        if match is None:
            return ''

        return match.group('path').strip()

    def _parse_comment(self, line: str) -> Optional[Comment]:
        match = self.COMMENT.match(line)
        if match is None:
            return None

        return Comment(
            time=match.group('time'),
            category=match.group('type'),
            comment=match.group('comment').strip()
        )
