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


from datetime import datetime
from pathlib import Path
from typing import Optional
from zipfile import ZipFile, ZIP_DEFLATED

from mpvqc import get_files
from mpvqc.doc_io.document import Document
from mpvqc.doc_io.output.combiner import DocumentCombiner
from mpvqc.doc_io.output.ingredients import DocumentIngredients
from mpvqc.doc_io.output.recipe import DocumentRecipe


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
    def construct_from(we_should_write: DocumentRecipe, that: DocumentIngredients) -> str:
        we = DocumentCombiner()
        we.write_file_tag()

        if we_should_write.header:
            if we_should_write.date:
                we.write_date(that.date)
            if we_should_write.generator:
                we.write_generator(that.generator)
            if we_should_write.nick:
                we.write_nick(that.nick)
            if we_should_write.path:
                we.write_path(that.path)

        we.write_empty_line()
        we.write_data_tag()
        we.write_comments(that.comments)
        we.write_comment_summary()
        we.write_empty_line()
        we.write_empty_line()

        return we.combine()

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
