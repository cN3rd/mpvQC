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


from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Tuple, List, Optional
from zipfile import ZipFile, ZIP_DEFLATED

from mpvqc import get_settings, get_metadata, get_files
from mpvqc.manager_new.comment import Comment
from mpvqc.manager_new.document import Document


class DocumentRecipe(NamedTuple):
    header: bool
    date: bool
    generator: bool
    nick: bool
    path: bool

    @staticmethod
    def from_settings() -> 'DocumentRecipe':
        s = get_settings()
        return DocumentRecipe(
            header=True,
            date=True,
            generator=True,
            nick=s.export_write_nickname,
            path=s.export_write_video_path
        )

    @staticmethod
    def for_backup() -> 'DocumentRecipe':
        return DocumentRecipe(
            header=True,
            date=True,
            generator=False,
            nick=False,
            path=True
        )


class DocumentIngredients(NamedTuple):
    date: str
    generator: str
    nick: str
    path: Optional[Path]
    comments: Tuple[Comment]

    @staticmethod
    def create_from(qc_document: Document) -> 'DocumentIngredients':
        s = get_settings()
        md = get_metadata()
        return DocumentIngredients(
            date=str(datetime.now().replace(microsecond=0)),
            generator=f'{md.app_name} {md.app_version}',
            nick=s.export_nickname,
            path=qc_document.video,
            comments=qc_document.comments
        )


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


class Exporter:

    @staticmethod
    def export(document: Document, to_path: Path) -> None:
        recipe = DocumentRecipe.from_settings()
        ingredients = DocumentIngredients.create_from(document)
        content = Exporter.construct_from(recipe, ingredients)
        Exporter._write(content, to_path)

    @staticmethod
    def backup(document: Document) -> None:
        recipe = DocumentRecipe.for_backup()
        ingredients = DocumentIngredients.create_from(document)
        content = Exporter.construct_from(recipe, ingredients)
        Exporter._backup(content, video=document.video)

    @staticmethod
    def construct_from(write: DocumentRecipe, data: DocumentIngredients) -> str:
        doc = DocumentCombiner()
        doc.write_file_tag()

        if write.header:
            if write.date:
                doc.write_date(data.date)
            if write.generator:
                doc.write_generator(data.generator)
            if write.nick:
                doc.write_nick(data.nick)
            if write.path:
                doc.write_path(data.path)

        doc.write_empty_line()
        doc.write_data_tag()
        doc.write_comments(data.comments)
        doc.write_comment_summary()
        doc.write_empty_line()
        doc.write_empty_line()

        return doc.combine()

    @staticmethod
    def _write(content: str, file: Path) -> None:
        file.write_text(content, encoding='utf-8')

    @staticmethod
    def _backup(content: str, video: Optional[Path]) -> None:
        files = get_files()
        now = datetime.now()

        zip_name = f'{now.year}-{now.month:02}.zip'
        zip_path = Path(files.dir_backup) / zip_name
        zip_file = ZipFile(zip_path, 'a' if zip_path.is_file() else 'w', compression=ZIP_DEFLATED)

        day = f'{now.year}-{now.month:02}-{now.day:02}'
        time = f'{now.hour:02}-{now.minute:02}-{now.second:02}'
        video = video.stem if video else 'unknown'

        file_name = f'{day}_{time}_{video}.txt'

        try:
            zip_file.writestr(file_name, content)
        finally:
            zip_file.close()
