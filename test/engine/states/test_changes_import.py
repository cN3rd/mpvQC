#  mpvQC
#
#  Copyright (C) 2021 mpvQC developers
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


import unittest
from pathlib import Path
from typing import Optional, Tuple

from mpvqc.engine.states import ImportChanges
from mpvqc.engine.states.changes_import import ImportEvaluator
from mpvqc.engine.states.state import InitialState, SavedState, UnsavedState, State
from test.doc_io.input import ANY_PATH, ANY_VIDEO


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.changes = ImportChanges()
        self.old_state: Optional[State] = None
        self.new_state: Optional[State] = None

    """ Startup """

    def we_start_in_initial_state(self, video=None, stored_video=None):
        self.old_state = InitialState(video, stored_video)

    def we_start_in_saved_state(self, file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple()):
        self.old_state = SavedState(file, video, stored_video, comments)

    def we_start_in_unsaved_state(self, file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple()):
        self.old_state = UnsavedState(file, video, stored_video, comments)

    """ Imports """

    def we_store_video(self, video: Optional[Path]):
        self.changes.stored_video = video

    def we_import_video(self, video: Optional[Path]):
        self.changes.loaded_video = video

    def we_import_document(self, document: Path):
        self.changes.loaded_documents = tuple([document])

    def we_import_documents(self, documents: Tuple[Path]):
        self.changes.loaded_documents = documents

    def we_clear_the_table(self):
        self.changes.cleared_the_table = True

    """ Evaluate """

    def we_evaluate_initial(self):
        evaluator = ImportEvaluator(self.changes, state=self.old_state, comments=tuple())
        self.new_state = evaluator.evaluate_initial()

    def we_evaluate_default(self):
        evaluator = ImportEvaluator(self.changes, state=self.old_state, comments=tuple())
        self.new_state = evaluator.evaluate_default()

    """ INITIAL (clean) -> Import 1x Video """

    def test_initial_then_import_video_assert_state(self):
        self.invoke_initial_import_video()
        self.assertFalse(self.new_state.has_changes())

    def test_initial_then_import_video_assert_video_path(self):
        imported_video = ANY_VIDEO
        self.invoke_initial_import_video(imported_video)
        self.assertEqual(imported_video, self.new_state.video)

    def test_initial_then_import_video_assert_document_path(self):
        imported_video = ANY_VIDEO
        self.invoke_initial_import_video(imported_video)
        self.assertIsNone(self.new_state.path)

    def invoke_initial_import_video(self, video=ANY_VIDEO):
        self.we_start_in_initial_state()
        self.we_import_video(video)
        self.we_evaluate_initial()

    """ INITIAL (clean) -> Import 1x Document without video """

    def test_initial_then_import_document_without_video_assert_state(self):
        self.invoke_initial_import_document_without_video()
        self.assertTrue(self.new_state.has_changes())

    def test_initial_then_import_document_without_video_assert_document_path(self):
        document = ANY_PATH
        self.invoke_initial_import_document_without_video(document)
        self.assertEqual(document, self.new_state.path)

    def invoke_initial_import_document_without_video(self, document=ANY_PATH):
        self.we_start_in_initial_state()
        self.we_import_document(document)
        self.we_evaluate_initial()

    """ INITIAL (clean) -> Import 1x Document with video stored in document """

    def test_initial_then_import_document_with_video_from_document_assert_state(self):
        self.invoke_initial_import_document_with_video_from_document()
        self.assertFalse(self.new_state.has_changes())

    def test_initial_then_import_document_with_video_from_document_assert_document_path(self):
        document = ANY_PATH
        self.invoke_initial_import_document_with_video_from_document(document)
        self.assertEqual(document, self.new_state.path)

    def test_initial_then_import_document_with_video_from_document_assert_video_path(self):
        video = ANY_VIDEO
        self.invoke_initial_import_document_with_video_from_document(video)
        self.assertEqual(video, self.new_state.video)

    def invoke_initial_import_document_with_video_from_document(self, document=ANY_PATH, video=ANY_VIDEO):
        self.we_start_in_initial_state()
        self.we_import_document(document)
        self.we_store_video(video)
        self.we_import_video(video)
        self.we_evaluate_initial()

    """ INITIAL (clean) -> Import 1x Document with video stored not in document """

    def test_initial_then_import_document_with_video_not_in_document_assert_state(self):
        self.invoke_initial_import_document_with_video_not_in_document()
        self.assertTrue(self.new_state.has_changes())

    def test_initial_then_import_document_with_video_not_in_document_assert_document_path(self):
        document = ANY_PATH
        self.invoke_initial_import_document_with_video_not_in_document(document)
        self.assertEqual(document, self.new_state.path)

    def test_initial_then_import_document_with_video_not_in_document_assert_video_path(self):
        video = ANY_VIDEO
        self.invoke_initial_import_document_with_video_not_in_document(video)
        self.assertEqual(video, self.new_state.video)

    def invoke_initial_import_document_with_video_not_in_document(self, document=ANY_PATH, video=ANY_VIDEO):
        self.we_start_in_initial_state()
        self.we_import_document(document)
        self.we_import_video(video)
        self.we_evaluate_initial()

    """ INITIAL (clean) -> Import multiple documents with video """

    def test_initial_then_import_multiple_documents_with_video_assert_state(self):
        documents = tuple([ANY_PATH, ANY_PATH])
        video = ANY_VIDEO
        self.invoke_initial_import_documents_with_video(documents, video)
        self.assertTrue(self.new_state.has_changes())

    def test_initial_then_import_multiple_documents_with_video_assert_document_path(self):
        documents = tuple([ANY_PATH, ANY_PATH])
        video = ANY_VIDEO
        self.invoke_initial_import_documents_with_video(documents, video)
        self.assertFalse(self.new_state.path)

    def test_initial_then_import_multiple_documents_with_video_assert_video_path(self):
        documents = tuple([ANY_PATH, ANY_PATH])
        video = ANY_VIDEO
        self.invoke_initial_import_documents_with_video(documents, video)
        self.assertTrue(self.new_state.video)

    def invoke_initial_import_documents_with_video(self, documents: Tuple[Path], video=ANY_VIDEO):
        self.we_start_in_initial_state()
        self.we_import_documents(documents)
        self.we_import_video(video)
        self.we_evaluate_initial()

    """ INITIAL (with video loaded already) -> Import document without video """

    def test_initial_with_video_then_import_document_without_video_assert_state(self):
        self.invoke_initial_with_video_import_document_without_video()
        self.assertTrue(self.new_state.has_changes())

    def test_initial_with_video_then_import_document_without_video_assert_document_path(self):
        self.invoke_initial_with_video_import_document_without_video()
        self.assertTrue(self.new_state.path)

    def test_initial_with_video_then_import_document_without_video_assert_video_path(self):
        video_before = ANY_VIDEO
        self.invoke_initial_with_video_import_document_without_video(video_present=video_before)
        self.assertEqual(video_before, self.new_state.video)

    def invoke_initial_with_video_import_document_without_video(self, video_present=ANY_VIDEO, document=ANY_PATH):
        self.we_start_in_initial_state(video=video_present)
        self.we_import_document(document)
        self.we_evaluate_initial()

    """ INITIAL (with video loaded already) -> Import document with video """

    def test_initial_with_video_then_import_document_with_video_assert_state(self):
        self.invoke_initial_with_video_import_document_with_video()
        self.assertFalse(self.new_state.has_changes())

    def test_initial_with_video_then_import_document_with_video_assert_document_path(self):
        document = ANY_PATH
        self.invoke_initial_with_video_import_document_with_video(document=document)
        self.assertEqual(document, self.new_state.path)

    def test_initial_with_video_then_import_document_with_video_assert_video_path(self):
        video_new = ANY_PATH
        self.invoke_initial_with_video_import_document_with_video(video_new=video_new)
        self.assertEqual(video_new, self.new_state.video)

    def invoke_initial_with_video_import_document_with_video(self,
                                                             video_present=ANY_VIDEO,
                                                             video_new=ANY_PATH,
                                                             document=ANY_PATH):
        self.we_start_in_initial_state(video=video_present)
        self.we_import_document(document)
        self.we_store_video(video_new)
        self.we_import_video(video_new)
        self.we_evaluate_initial()

    """ DEFAULT -> Import 1x video """

    def test_default_then_import_video_assert_state(self):
        video_new = ANY_VIDEO
        self.invoke_default_import_video(video_new)
        self.assertTrue(self.new_state.has_changes())

    def test_default_then_import_video_assert_video_path(self):
        video_new = ANY_VIDEO
        self.invoke_default_import_video(video_new)
        self.assertEqual(video_new, self.new_state.video)

    def test_default_then_import_video_assert_document_path(self):
        video_new = ANY_VIDEO
        self.invoke_default_import_video(video_new)
        self.assertIsNone(self.new_state.path)

    def invoke_default_import_video(self, video=ANY_VIDEO):
        self.we_start_in_saved_state()
        self.we_import_video(video)
        self.we_evaluate_default()

    """ DEFAULT -> Import 1x Document without video """

    def test_default_then_import_document_without_video_assert_state(self):
        self.invoke_default_import_document_without_video()
        self.assertTrue(self.new_state.has_changes())

    def test_default_then_import_document_without_video_assert_document_path(self):
        document = ANY_PATH
        self.invoke_default_import_document_without_video(document)
        self.assertFalse(self.new_state.path)

    def invoke_default_import_document_without_video(self, document=ANY_PATH):
        self.we_start_in_saved_state()
        self.we_import_document(document)
        self.we_evaluate_default()

    """ DEFAULT -> Import 1x Document with video stored in document (without clearing the table) """

    def test_default_then_import_document_with_video_from_document_without_clearing_table_assert_state(self):
        self.invoke_default_import_document_with_video_from_document_without_clearing_table()
        self.assertTrue(self.new_state.has_changes())

    def test_default_then_import_document_with_video_from_document_without_clearing_table_assert_document_path(self):
        document = ANY_PATH
        self.invoke_default_import_document_with_video_from_document_without_clearing_table(document)
        self.assertFalse(self.new_state.path)

    def test_default_then_import_document_with_video_from_document_without_clearing_table_assert_video_path(self):
        video = ANY_VIDEO
        self.invoke_default_import_document_with_video_from_document_without_clearing_table(video)
        self.assertEqual(video, self.new_state.video)

    def invoke_default_import_document_with_video_from_document_without_clearing_table(self,
                                                                                       document=ANY_PATH,
                                                                                       video=ANY_VIDEO):
        self.we_start_in_saved_state()
        self.we_import_document(document)
        self.we_store_video(video)
        self.we_import_video(video)
        self.we_evaluate_default()

    """ DEFAULT -> Import 1x Document with video stored in document (with clearing the table) """

    def test_default_then_import_document_with_video_from_document_with_clearing_table_assert_state(self):
        self.invoke_default_import_document_with_video_from_document_with_clearing_table()
        self.assertFalse(self.new_state.has_changes())

    def test_default_then_import_document_with_video_from_document_with_clearing_table_assert_document_path(self):
        document = ANY_PATH
        self.invoke_default_import_document_with_video_from_document_with_clearing_table(document)
        self.assertEqual(document, self.new_state.path)

    def test_default_then_import_document_with_video_from_document_with_clearing_table_assert_video_path(self):
        video = ANY_VIDEO
        self.invoke_default_import_document_with_video_from_document_with_clearing_table(video)
        self.assertEqual(video, self.new_state.video)

    def invoke_default_import_document_with_video_from_document_with_clearing_table(self,
                                                                                    document=ANY_PATH,
                                                                                    video=ANY_VIDEO):
        self.we_start_in_saved_state()
        self.we_import_document(document)
        self.we_clear_the_table()
        self.we_store_video(video)
        self.we_import_video(video)
        self.we_evaluate_default()

    """ DEFAULT -> Import 1x Document with video stored not in document (without clearing the table)"""

    def test_default_then_import_document_with_video_not_in_document_without_clearing_table_assert_state(self):
        self.invoke_default_import_document_with_video_not_in_document_without_clearing_table()
        self.assertTrue(self.new_state.has_changes())

    def test_default_then_import_document_with_video_not_in_document_without_clearing_table_assert_document_path(self):
        document = ANY_PATH
        self.invoke_default_import_document_with_video_not_in_document_without_clearing_table(document)
        self.assertIsNone(self.new_state.path)

    def test_default_then_import_document_with_video_not_in_document_without_clearing_table_assert_video_path(self):
        video = ANY_VIDEO
        self.invoke_default_import_document_with_video_not_in_document_without_clearing_table(video)
        self.assertEqual(video, self.new_state.video)

    def invoke_default_import_document_with_video_not_in_document_without_clearing_table(self,
                                                                                         document=ANY_PATH,
                                                                                         video=ANY_VIDEO):
        self.we_start_in_saved_state()
        self.we_import_document(document)
        self.we_import_video(video)
        self.we_evaluate_default()

    """ DEFAULT -> Import 1x Document with video stored not in document (with clearing the table)"""

    def test_default_then_import_document_with_video_not_in_document_with_clearing_table_assert_state(self):
        self.invoke_default_import_document_with_video_not_in_document_with_clearing_table()
        self.assertTrue(self.new_state.has_changes())

    def test_default_then_import_document_with_video_not_in_document_with_clearing_table_assert_document_path(self):
        document = ANY_PATH
        self.invoke_default_import_document_with_video_not_in_document_with_clearing_table(document)
        self.assertEqual(document, self.new_state.path)

    def test_default_then_import_document_with_video_not_in_document_with_clearing_table_assert_video_path(self):
        video = ANY_VIDEO
        self.invoke_default_import_document_with_video_not_in_document_with_clearing_table(video)
        self.assertEqual(video, self.new_state.video)

    def invoke_default_import_document_with_video_not_in_document_with_clearing_table(self,
                                                                                      document=ANY_PATH,
                                                                                      video=ANY_VIDEO):
        self.we_start_in_saved_state()
        self.we_import_document(document)
        self.we_clear_the_table()
        self.we_import_video(video)
        self.we_evaluate_default()

    """ DEFAULT -> Import multiple documents with video """

    def test_default_then_import_multiple_documents_with_video_assert_state(self):
        documents = tuple([ANY_PATH, ANY_PATH])
        video = ANY_VIDEO
        self.invoke_default_import_documents_with_video(documents, video)
        self.assertTrue(self.new_state.has_changes())

    def test_default_then_import_multiple_documents_with_video_assert_document_path(self):
        documents = tuple([ANY_PATH, ANY_PATH])
        video = ANY_VIDEO
        self.invoke_default_import_documents_with_video(documents, video)
        self.assertIsNone(self.new_state.path)

    def test_default_then_import_multiple_documents_with_video_assert_video_path(self):
        documents = tuple([ANY_PATH, ANY_PATH])
        video = ANY_VIDEO
        self.invoke_default_import_documents_with_video(documents, video)
        self.assertTrue(self.new_state.video)

    def invoke_default_import_documents_with_video(self, documents: Tuple[Path], video=ANY_VIDEO):
        self.we_start_in_saved_state()
        self.we_import_documents(documents)
        self.we_import_video(video)
        self.we_evaluate_default()
