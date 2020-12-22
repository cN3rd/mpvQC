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


class Comment:

    def __init__(self, time: str, category: str, comment: str):
        self.comment_note = comment.strip()
        self.comment_type = category.strip()
        self.comment_time = time.strip()

    def __str__(self):
        return f"[{self.comment_time}] [{self.comment_type}] {self.comment_note}".strip()

    def __repr__(self):
        return f"[{self.comment_time}] [{self.comment_type}] {self.comment_note[:10]}".strip()

    def __eq__(self, other):
        return isinstance(other, Comment) \
               and self.comment_time == other.comment_time \
               and self.comment_type == other.comment_type \
               and self.comment_note == other.comment_note

    def __lt__(self, other):
        return isinstance(other, Comment) \
               and (self.comment_time, self.comment_type.lower(), self.comment_note.lower()) < \
               (other.comment_time, other.comment_type.lower(), other.comment_note.lower())
