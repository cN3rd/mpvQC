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

from mpvqc.doc_io import Document, Incompatible
from mpvqc.core import Comment

ANY_PATH: Path = Path('mpvQC') / 'ANY' / 'PATH'
ANY_VIDEO: Path = Path('mpvQC') / 'ANY' / 'VIDEO.MP4'
ANY_COMMENT: Comment = Comment(time="00:00:00", category="Spelling", comment="this, that")

ANY_DOCUMENT: Document = Document(ANY_PATH, video=None, comments=tuple())
ANY_INCOMPATIBLE: Incompatible = Incompatible(file=ANY_PATH)
