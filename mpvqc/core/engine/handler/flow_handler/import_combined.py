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

from mpvqc.core.engine.handler import FlowHandler
from mpvqc.core.engine.handler.flow_handler.import_document import DocumentImportFlowHandler
from mpvqc.core.engine.handler.flow_handler.import_subtitles import SubtitleImportFlowHandler
from mpvqc.core.engine.handler.flow_handler.import_video import VideoImportFlowHandler
from mpvqc.core.engine.interface import Options
from mpvqc.core.engine.states import ImportChanges


class CombinedImportFlowHandler(FlowHandler):

    def __init__(
            self,
            document_paths: Tuple[Path] = tuple(),
            video_path: Optional[Path] = None,
            subtitle_paths: Tuple[Path] = tuple()
    ):
        self._document_paths = document_paths
        self._video_path = video_path
        self._subtitle_paths = subtitle_paths

        self._changes = ImportChanges()

    def handle_flow_with(self, options: Options) -> None:
        importer = DocumentImportFlowHandler(self._document_paths,
                                             load_linked_video=self.only_if_user_has_not_supplied_a_video())
        if importer.has_document_paths():
            importer.handle_flow_with(options)

            if importer.has_abort_called():
                return

            self._changes = self._changes.combine_with(importer.get_changes())

        importer = VideoImportFlowHandler(self._video_path)
        if importer.has_video_path():
            importer.handle_flow_with(options)

            self._changes = self._changes.combine_with(importer.get_changes())

        importer = SubtitleImportFlowHandler(self._subtitle_paths)
        if importer.has_subtitle_paths():
            importer.handle_flow_with(options)

    def only_if_user_has_not_supplied_a_video(self) -> bool:
        return not self._user_has_supplied_a_video()

    def _user_has_supplied_a_video(self) -> bool:
        return bool(self._video_path)

    def get_changes(self) -> ImportChanges:
        return self._changes

