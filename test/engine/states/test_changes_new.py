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


from mpvqc.engine.states.changes_new import NewDocumentChanges, NewDocumentEvaluator
from mpvqc.engine.states.state import InitialState, SavedState, UnsavedState
from test.doc_io.input import ANY_PATH, ANY_VIDEO


UNCHANGED = NewDocumentChanges()
UNCHANGED.cleared_the_table = False

CHANGED = NewDocumentChanges()
CHANGED.cleared_the_table = True


INITIAL = InitialState(video=None, stored_video=None)
SAVED = SavedState(file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple())
UNSAVED = UnsavedState(file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple())


class Test(unittest.TestCase):

    def test_unchanged_initial(self):
        old_state = INITIAL

        evaluator = NewDocumentEvaluator(UNCHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.has_changes(), new_state.has_changes())

    def test_unchanged_saved(self):
        old_state = SAVED

        evaluator = NewDocumentEvaluator(UNCHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.has_changes(), new_state.has_changes())

    def test_unchanged_unsaved(self):
        old_state = UNSAVED

        evaluator = NewDocumentEvaluator(UNCHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.has_changes(), new_state.has_changes())

    def test_changed_initial(self):
        old_state = INITIAL

        evaluator = NewDocumentEvaluator(CHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.has_changes(), new_state.has_changes())

    def test_changed_saved_assert_no_changes(self):
        old_state = SAVED

        evaluator = NewDocumentEvaluator(CHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertFalse(new_state.has_changes())

    def test_changed_saved_assert_video_path(self):
        old_state = SAVED

        evaluator = NewDocumentEvaluator(CHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.video, new_state.video)

    def test_changed_saved_assert_document_path(self):
        old_state = SAVED

        evaluator = NewDocumentEvaluator(CHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertNotEqual(old_state.path, new_state.path)

    def test_changed_unsaved_assert_no_changes(self):
        old_state = UNSAVED

        evaluator = NewDocumentEvaluator(CHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertFalse(new_state.has_changes())

    def test_changed_unsaved_assert_video_path(self):
        old_state = UNSAVED

        evaluator = NewDocumentEvaluator(CHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.video, new_state.video)

    def test_changed_unsaved_assert_document_path(self):
        old_state = UNSAVED

        evaluator = NewDocumentEvaluator(CHANGED, old_state)
        new_state = evaluator.evaluate()

        self.assertNotEqual(old_state.path, new_state.path)


