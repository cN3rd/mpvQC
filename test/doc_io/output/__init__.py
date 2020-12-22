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
from typing import NamedTuple

from mpvqc.doc_io.output.ingredients import DocumentIngredients
from mpvqc.doc_io.output.recipe import DocumentRecipe
from mpvqc.core import Comment


class MockedSettings(NamedTuple):
    export_write_nickname: bool = True
    export_write_video_path: bool = True
    export_nickname: str = "test-nickname"


class MockedMetadata(NamedTuple):
    app_name: str = "app-name"
    app_version: str = "0.0.7"


class MockedFiles(NamedTuple):
    dir_backup: str = str(Path.home())


class TestData:
    recipe_all = DocumentRecipe(header=True, date=True, generator=True, nick=True, path=True)
    recipe_no_header = DocumentRecipe(header=False, date=True, generator=True, nick=True, path=True)
    recipe_no_nick = DocumentRecipe(header=True, date=True, generator=True, nick=False, path=True)
    recipe_no_path = DocumentRecipe(header=True, date=True, generator=True, nick=True, path=False)

    ingredients = DocumentIngredients(
        date='01.01.1970',
        generator='10km a day',
        nick='saitama',
        path=Path('10 km'),
        comments=(Comment(time="00:00:00", category="ok", comment="ok"),)
    )
    export_path = Path.home()