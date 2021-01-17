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
from typing import List

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from mpvqc.core.engine.handler.backup import Backup
from mpvqc.core.engine.interface import AppImpl, PlayerImpl, TableImpl, Options
from mpvqc.widgets import CommentsTable, MpvWidget


class QcManager(QObject):
    """"""

    """Signal, that indicates a modifications change. p1='new modifications (saved/unsaved)'"""
    state_changed = pyqtSignal(bool)

    """Signal, that indicates a new video import. p1='new video path'"""
    video_imported = pyqtSignal(Path)

    def __init__(self, app: QMainWindow, mpv_widget: MpvWidget, table: CommentsTable):
        super(QcManager, self).__init__()

        app = AppImpl(app)
        player = PlayerImpl(mpv_widget.player)
        table = TableImpl(table)
        options = Options(app, player, table)

        table.comments_modified.connect(lambda func=self._on_table_content_modified: func())

        from mpvqc.core.engine.state_manager import StateManager
        self._app_state = StateManager(options)
        self._app_state.state_changed.connect(self.state_changed.emit)
        self._app_state.video_imported.connect(self.video_imported.emit)

        self._backupper = Backup(options=options)

    def _on_table_content_modified(self, *_):
        self._app_state.on_comments_modified()

    def has_changes(self) -> bool:
        return self._app_state.has_changes()

    def request_new_document(self):
        self._app_state.on_new_document()

    def request_open_qc_documents(self):
        self._app_state.on_import_documents()

    def request_open_video(self):
        self._app_state.on_import_video()

    def request_open_subtitles(self):
        self._app_state.on_import_subtitles()

    def request_save_qc_document(self):
        self._app_state.on_save()

    def request_save_qc_document_as(self):
        self._app_state.on_save_as()

    def request_quit_application(self) -> bool:
        return self._app_state.on_quit()

    def do_open_drag_and_drop_data(self, vids: List[str], docs: List[str], subs: List[str]):
        video = Path(vids[0]) if vids else None
        documents = tuple(map(Path, docs))
        subtitles = tuple(map(Path, subs))
        self._app_state.on_drag_and_drop(documents, video, subtitles)

    def reset_auto_save(self):
        self._backupper.reset_timer()
