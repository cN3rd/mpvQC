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
from typing import TextIO

from mpvqc.doc_io import Document
from mpvqc.doc_io.input.error import NotADocumentError
from mpvqc.doc_io.input.parser import DocumentLineParser


class FileReader:
    PREFIX = '[FILE]'

    def __init__(self, file: Path):
        self._file = file
        self._parser = DocumentLineParser()

    def read(self) -> None:
        with self._file.open('r', encoding='utf-8-sig') as lines:
            self._process(lines)

    def _process(self, lines: TextIO):
        self._validate_first_of(lines)
        self._read_rest_of(lines)

    def _validate_first_of(self, lines: TextIO):
        self._validate(lines.readline())

    def _validate(self, line: str):
        if self._is_not_valid_first(line.strip()):
            raise NotADocumentError(self._file)

    def _is_not_valid_first(self, line: str):
        return not self._is_valid_first(line)

    def _is_valid_first(self, line: str):
        return line.startswith(self.PREFIX)

    def _read_rest_of(self, lines: TextIO):
        for line in lines:
            self._process_each(line)

    def _process_each(self, line: str):
        self._parse(line.strip())

    def _parse(self, line: str):
        self._parser.parse(line)

    def get_document(self) -> Document:
        return Document(
            file=self._file,
            video=self._parser.get_video(),
            comments=self._parser.get_comments()
        )
