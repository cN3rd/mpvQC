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


import re
from pathlib import Path
from typing import List, Optional, Tuple

from mpvqc.core import Comment


class DocumentLineParser:
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

    def get_video(self) -> Optional[Path]:
        return Path(self._video) if self._video else None

    def get_comments(self) -> Tuple[Comment]:
        return tuple(self._comments)
