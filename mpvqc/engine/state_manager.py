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


from contextlib import contextmanager
from pathlib import Path
from typing import Tuple, Optional, Callable

from PyQt5.QtCore import pyqtSignal, QObject

from mpvqc.engine.handler import FlowHandler
from mpvqc.engine.handler.flow_handler import \
    CombinedImportFlowHandler, \
    DocumentImportFlowHandler, \
    VideoImportFlowHandler, \
    SubtitleImportFlowHandler, \
    QuitQuestionFlowHandler, \
    NewDocumentFlowHandler, \
    ModifyCommentsFlowHandler, \
    SaveDocumentFlowHandler
from mpvqc.engine.interface import Options
from mpvqc.engine.states import State, initial_state


class StateManager(QObject):
    """"""

    """Signal, that indicates a modifications change. p1='new modifications (saved/unsaved)'"""
    state_changed = pyqtSignal(bool)

    """Signal, that indicates a new video import. p1='new video path'"""
    video_imported = pyqtSignal(Path)

    def __init__(self, options: Options):
        super().__init__()
        self._options = options
        self._state_current: State = initial_state()
        self._state_last_saved = self._state_current

        self._fire_signals: bool = True

    @contextmanager
    def _signal_barrier(self):
        self._fire_signals = False
        yield
        self._fire_signals = True

    def has_changes(self):
        return self._state_current.has_changes()

    def on_comments_modified(self):
        if self._fire_signals:
            self._execute(handler=ModifyCommentsFlowHandler(),
                          evaluate_with=self._state_current.evaluate_comments_modification)

    def on_save(self):
        self._execute(handler=SaveDocumentFlowHandler(self._state_current.path),
                      evaluate_with=self._state_current.evaluate_save)

    def on_save_as(self):
        self._execute(handler=SaveDocumentFlowHandler(current_file=None),
                      evaluate_with=self._state_current.evaluate_save)

    def on_new_document(self):
        self._execute(handler=NewDocumentFlowHandler(have_unsaved_changes=self.has_changes()),
                      evaluate_with=self._state_current.evaluate_new_document)

    def on_import_documents(self):
        self._execute(handler=DocumentImportFlowHandler(),
                      evaluate_with=self._state_current.evaluate_import)

    def on_import_video(self):
        self._execute(handler=VideoImportFlowHandler(),
                      evaluate_with=self._state_current.evaluate_import)

    def on_import_subtitles(self):
        self._execute(handler=SubtitleImportFlowHandler(),
                      evaluate_with=self._state_current.evaluate_import)

    def on_drag_and_drop(self, documents: Tuple[Path], video: Optional[Path], subtitles: Tuple[Path]):
        self._execute(handler=CombinedImportFlowHandler(documents, video, subtitles),
                      evaluate_with=self._state_current.evaluate_import)

    def on_quit(self):
        return QuitQuestionFlowHandler(have_unsaved_changes=self.has_changes()).ask_with(self._options)

    def _execute(self, handler: FlowHandler, evaluate_with: Callable[[any, Options], State]) -> None:
        with self._signal_barrier():
            handler.handle_flow_with(self._options)
            changes = handler.get_changes()

        self._state_current = evaluate_with(changes, self._options)

        self._evaluate_state_change()
        self._evaluate_video_change(_from=changes)

    def _evaluate_state_change(self):
        if self._state_current.saved:
            self._state_last_saved = self._state_current
        elif self._state_last_saved == self._state_current:
            self._state_current = self._state_last_saved
        self.state_changed.emit(self._state_current.has_changes())

    def _evaluate_video_change(self, _from: any):
        video = getattr(_from, 'loaded_video', None)
        if video:
            self.video_imported.emit(video)
