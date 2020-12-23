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


from typing import Tuple, Iterable

from PyQt5.QtCore import pyqtSignal, QObject

from mpvqc.core import Comment
from mpvqc.engine.interface.table import Table
from mpvqc.widgets import CommentsTable


class TableImpl(Table, QObject):

    """Signal gets emitted every time the table fires a change event """
    comments_modified = pyqtSignal()

    def __init__(self, table: CommentsTable):
        super().__init__()
        self._table = table
        self._table.comments_changed.connect(lambda value, fun=self.comments_modified.emit: fun())

    def has_comments(self) -> bool:
        return bool(self._table.get_all_comments())

    def add(self, comments: Iterable[Comment]) -> None:
        self._table.add_comments(tuple(comments))

    def get_all_comments(self) -> Tuple[Comment]:
        return self._table.get_all_comments()

    def clear_comments(self) -> None:
        self._table.reset_comments_table()
