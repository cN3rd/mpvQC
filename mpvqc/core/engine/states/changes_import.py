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
from typing import Tuple, Optional

from mpvqc.core import Comment
from mpvqc.core.engine.states.state import State, InitialState, SavedState, UnsavedState


class ImportChanges:

    def __init__(self):
        self.cleared_the_table: bool = False
        self.stored_video: Optional[Path] = None
        self.loaded_video: Optional[Path] = None
        self.loaded_documents: Tuple[Path] = tuple()

    def __eq__(self, other):
        return isinstance(other, ImportChanges) \
               and self.cleared_the_table == other.cleared_the_table \
               and self.stored_video == other.stored_video \
               and self.loaded_video == other.loaded_video \
               and self.loaded_documents == other.loaded_documents

    def combine_with(self, other: 'ImportChanges') -> 'ImportChanges':
        new = ImportChanges()
        new.cleared_the_table = other.cleared_the_table or self.cleared_the_table
        new.stored_video = other.stored_video or self.stored_video
        new.loaded_video = other.loaded_video or self.loaded_video
        new.loaded_documents = other.loaded_documents or self.loaded_documents
        return new


class ImportChangesEvaluator:
    UNCHANGED = ImportChanges()

    def __init__(self, changes: ImportChanges):
        self._changes = changes

    @property
    def stored_video(self) -> Optional[Path]:
        return self._changes.stored_video

    @property
    def loaded_video(self) -> Optional[Path]:
        return self._changes.loaded_video

    @property
    def loaded_document(self) -> Optional[Path]:
        return self._changes.loaded_documents[0] if self._changes.loaded_documents else None

    def havent_done_anything(self) -> bool:
        return self._changes == self.UNCHANGED

    def have_cleared_the_table(self) -> bool:
        return self._changes.cleared_the_table

    def have_stored_a_video(self) -> bool:
        return bool(self.stored_video)

    def havent_stored_a_video(self) -> bool:
        return not self.have_stored_a_video()

    def have_stored_the_video(self, maybe: Optional[Path]) -> bool:
        return self.stored_video.resolve() == maybe.resolve() if self.stored_video and maybe else False

    def have_loaded_the_video(self, maybe: Optional[Path]) -> bool:
        return self.loaded_video.resolve() == maybe.resolve() if self.loaded_video and maybe else False

    def have_loaded_the_stored_video(self, stored: Optional[Path] = None) -> bool:
        if stored is None:
            stored: Optional[Path] = self.stored_video
            if stored is None:
                return False
        return self.have_loaded_the_video(maybe=stored)

    def have_loaded_one_document(self) -> bool:
        return len(self._changes.loaded_documents) == 1

    def have_loaded_more_than_one_document(self) -> bool:
        return len(self._changes.loaded_documents) > 1


class ImportEvaluator:

    def __init__(self, changes: ImportChanges, state: State, comments: Tuple[Comment]):
        self._we = ImportChangesEvaluator(changes)
        self._current = state
        self._comments = comments

    def evaluate_initial(self) -> State:
        we, the_new, current, comments = self._we, self._we, self._current, self._comments

        if we.havent_done_anything():
            return current

        video = the_new.loaded_video or current.video
        stored_video = (the_new.stored_video or current.stored_video) if not video else None

        if we.have_loaded_one_document():
            if we.have_stored_a_video() and we.have_loaded_the_stored_video():
                return SavedState(
                    file=the_new.loaded_document,
                    video=the_new.loaded_video,
                    stored_video=None,
                    comments=comments
                )
            elif we.have_stored_the_video(maybe=current.video):
                return SavedState(
                    file=the_new.loaded_document,
                    video=current.video,
                    stored_video=None,
                    comments=comments
                )
            elif we.havent_stored_a_video():
                return UnsavedState(
                    file=the_new.loaded_document,
                    video=video,
                    stored_video=stored_video,
                    comments=comments
                )
        elif we.have_loaded_more_than_one_document():
            pass
        else:
            return InitialState(
                video=video,
                stored_video=stored_video
            )

        return UnsavedState(
            file=None,
            video=video,
            stored_video=stored_video,
            comments=comments
        )

    def evaluate_default(self) -> State:
        we, the_new, current, comments = self._we, self._we, self._current, self._comments

        if we.havent_done_anything():
            return current

        if we.have_cleared_the_table():
            return self.evaluate_initial()

        video = the_new.loaded_video or current.video
        stored_video = (the_new.stored_video or current.stored_video) if not video else None

        if we.have_loaded_one_document():
            pass
        elif we.have_loaded_more_than_one_document():
            pass
        else:
            if we.have_loaded_the_stored_video(current.stored_video):
                return current.on_stored_video_was_loaded()

        return UnsavedState(
            file=None,
            video=video,
            stored_video=stored_video,
            comments=comments
        )
