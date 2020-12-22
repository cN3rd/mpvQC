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


from abc import abstractmethod
from typing import Tuple

from mpvqc.core import Comment


class Table:

    @abstractmethod
    def has_comments(self) -> bool:
        pass

    @abstractmethod
    def add(self, comments: Tuple[Comment]):
        pass

    @abstractmethod
    def get_all_comments(self) -> Tuple[Comment]:
        pass

    @abstractmethod
    def clear_comments(self) -> None:
        pass
