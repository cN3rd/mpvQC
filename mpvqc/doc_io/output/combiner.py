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


from pathlib import Path
from typing import List, Optional, Tuple

from mpvqc.engine.comment import Comment


class DocumentCombiner:

    def __init__(self):
        self._lines: List[str] = []
        self._total_comments = 0

    def write_file_tag(self) -> None:
        self._lines.append('[FILE]')

    def write_date(self, date: str) -> None:
        self._lines.append(f'date      : {date}')

    def write_generator(self, generator: str) -> None:
        self._lines.append(f'generator : {generator}')

    def write_nick(self, nick: str) -> None:
        self._lines.append(f'nick      : {nick}')

    def write_path(self, path: Optional[Path]) -> None:
        self._lines.append(f'path      : {str(path if path else "")}')

    def write_empty_line(self) -> None:
        self._lines.append('')

    def write_data_tag(self) -> None:
        self._lines.append('[DATA]')

    def write_comments(self, comments: Tuple[Comment]) -> None:
        self._total_comments = self._total_comments + len(comments)
        for comment in comments:
            self._lines.append(str(comment))

    def write_comment_summary(self) -> None:
        self._lines.append(f'# total lines: {self._total_comments}')

    def combine(self) -> str:
        return '\n'.join(self._lines)
