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


from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, Optional

from mpvqc.core import Comment
from mpvqc.core.engine.interface import Options


class State(ABC):

    def __init__(
            self,
            file: Optional[Path],
            video: Optional[Path],
            stored_video: Optional[Path],
            comments: Tuple[Comment],
            saved: bool
    ):
        self._file: Optional[Path] = file
        self._video: Optional[Path] = video
        self._stored_video: Optional[Path] = stored_video
        self._comments: Tuple[Comment] = comments
        self._saved = saved

    def __eq__(self, other):
        return isinstance(other, State) \
               and self._file == other._file \
               and self._video == other._video \
               and self._comments == other._comments

    def __str__(self):
        return f'Document path       : {self._file}\n' \
               f'Video path          : {self._video}\n' \
               f'Video path (stored) : {self._stored_video}\n' \
               f'Comments            : {len(self._comments)}\n' \
               f'Saved:              : {self._saved}'

    @property
    def path(self):
        return self._file

    @property
    def video(self):
        return self._video

    @property
    def stored_video(self):
        return self._stored_video

    @property
    def comments(self):
        return self._comments

    @property
    def saved(self) -> bool:
        return self._saved

    def has_changes(self) -> bool:
        return not self.saved

    @abstractmethod
    def on_stored_video_was_loaded(self) -> 'State':
        pass

    def evaluate_comments_modification(self, changes, options: Options) -> 'State':
        from mpvqc.core.engine.states.changes_comments import CommentsEvaluator
        return CommentsEvaluator(changes, state=self, comments=options.table.get_all_comments()).evaluate()

    def evaluate_new_document(self, changes, __: Options) -> 'State':
        from mpvqc.core.engine.states.changes_new import NewDocumentEvaluator
        return NewDocumentEvaluator(changes, state=self).evaluate()

    def evaluate_save(self, changes, options: Options) -> 'State':
        from mpvqc.core.engine.states.changes_save import SaveEvaluator
        return SaveEvaluator(changes, state=self, comments=options.table.get_all_comments()).evaluate()

    def evaluate_import(self, changes, options: Options) -> 'State':
        from mpvqc.core.engine.states.changes_import import ImportEvaluator
        return ImportEvaluator(changes, state=self, comments=options.table.get_all_comments()).evaluate_default()


class InitialState(State):
    """
    The state the document/application has, when no comments are available or now document was imported.
    The state should also be initial, when the user resets the document state by pressing the 'New' button.
    """

    def __init__(self, video: Optional[Path], stored_video: Optional[Path]):
        super().__init__(file=None, video=video, stored_video=stored_video, comments=tuple(), saved=True)

    def on_stored_video_was_loaded(self) -> State:
        return InitialState(video=self.stored_video, stored_video=None)

    def evaluate_import(self, changes, options: Options) -> State:
        from mpvqc.core.engine.states.changes_import import ImportEvaluator
        return ImportEvaluator(changes, state=self, comments=options.table.get_all_comments()).evaluate_initial()


class SavedState(State):

    def __init__(
            self,
            file: Optional[Path],
            video: Optional[Path],
            stored_video: Optional[Path],
            comments: Tuple[Comment]
    ):
        super().__init__(file, video, stored_video, comments, saved=True)

    def on_stored_video_was_loaded(self) -> State:
        return SavedState(file=self.path, video=self.stored_video, stored_video=None, comments=self.comments)


class UnsavedState(State):

    def __init__(
            self,
            file: Optional[Path],
            video: Optional[Path],
            stored_video: Optional[Path],
            comments: Tuple[Comment]
    ):
        super().__init__(file, video, stored_video, comments, saved=False)

    def on_stored_video_was_loaded(self) -> State:
        return UnsavedState(file=self.path, video=self.stored_video, stored_video=None, comments=self.comments)
