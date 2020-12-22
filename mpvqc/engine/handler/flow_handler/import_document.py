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
from typing import Tuple

from mpvqc.engine.handler import FlowHandler
from mpvqc.engine.handler.flow_actions import DocumentImportFlowActions, VideoImportFlowActions
from mpvqc.engine.interface import Options
from mpvqc.engine.states import ImportChanges


class DocumentImportFlowHandler(FlowHandler):

    def __init__(self, document_paths: Tuple[Path] = tuple(), load_linked_video: bool = True):
        self._document_paths = document_paths

        self._imported_documents_compatible: Tuple[Path] = tuple()
        self._linked_videos: Tuple[Path] = tuple()

        self._abort_import_called = False
        self._load_linked_video = load_linked_video

        self._changes = ImportChanges()

    def get_changes(self) -> ImportChanges:
        return self._changes

    def has_document_paths(self) -> bool:
        return bool(self._document_paths)

    def has_abort_called(self) -> bool:
        return self._abort_import_called

    def handle_flow_with(self, options: Options) -> None:
        self._handle_document_import_with(options)
        self._handle_video_import_with(options)

    def _handle_document_import_with(self, options: Options) -> None:
        we = DocumentImportFlowActions(options, self._document_paths)

        if we.dont_have_any_paths():
            we.ask_via_dialog_for_paths()

        if we.have_any_paths():
            we.import_paths()

        if we.neither_have_documents_nor_incompatibles_imported():
            return

        if we.have_documents_imported():

            if we.have_comments():
                we.ask_via_message_box_what_to_do_with_comments()

                if we.want_to_abort_the_import():
                    self._abort_import_called = True
                    return

                elif we.want_to_clear_all_comments():
                    we.clear_all_comments()

            we.load_comments()

        if we.have_incompatibles_imported():
            we.show_via_message_box_all_incompatible_documents()

        self._linked_videos = we.get_the_found_videos()
        self._imported_documents_compatible = we.get_all_paths_from_imported_documents()

        self._changes = self._changes.combine_with(we.get_changes())

    def _handle_video_import_with(self, options: Options) -> None:
        if self._we_are_not_supposed_to_load_the_video():
            return

        we = VideoImportFlowActions(options, self._linked_videos[0])
        if we.confirm_the_video_exists():

            if we.see_the_video_is_not_already_playing():
                we.ask_via_message_box_to_open_found_video()

                if we.want_to_open_found_video():
                    we.load_video()

        self._changes = self._changes.combine_with(we.get_changes())

    def _we_are_not_supposed_to_load_the_video(self) -> bool:
        return self._abort_called() \
               or self._no_video_was_found() \
               or self._more_than_one_document_imported() \
               or self._we_got_the_instruction_from_outside()

    def _abort_called(self) -> bool:
        return self._abort_import_called

    def _no_video_was_found(self) -> bool:
        return len(self._linked_videos) == 0

    def _more_than_one_document_imported(self) -> bool:
        return len(self._imported_documents_compatible) > 1

    def _we_got_the_instruction_from_outside(self) -> bool:
        return not self._load_linked_video
