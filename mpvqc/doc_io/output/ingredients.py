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
from typing import NamedTuple, Optional, Tuple

from mpvqc import get_settings, get_metadata
from mpvqc.engine.comment import Comment
from mpvqc.doc_io.document import Document


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
