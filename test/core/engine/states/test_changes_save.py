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

from mpvqc.core.engine.states.changes_save import SaveChanges, SaveEvaluator
from mpvqc.core.engine.states.state import InitialState, SavedState, UnsavedState
from test.doc_io.input import ANY_PATH, ANY_VIDEO

UNCHANGED = SaveChanges()
UNCHANGED.save_path = None

CHANGED = SaveChanges()
CHANGED.save_path = ANY_PATH

INITIAL = InitialState(video=None, stored_video=None)
SAVED = SavedState(file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple())
UNSAVED = UnsavedState(file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple())


class Test(unittest.TestCase):

    def test_unchanged_initial(self):
        old_state = INITIAL

        evaluator = SaveEvaluator(UNCHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.has_changes(), new_state.has_changes())

    def test_unchanged_saved(self):
        old_state = SAVED

        evaluator = SaveEvaluator(UNCHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.has_changes(), new_state.has_changes())

    def test_unchanged_unsaved_with_path(self):
        old_state = UnsavedState(file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple())

        evaluator = SaveEvaluator(UNCHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertFalse(new_state.has_changes())

    def test_unchanged_unsaved_without_path(self):
        old_state = UnsavedState(file=None, video=ANY_VIDEO, stored_video=None, comments=tuple())

        evaluator = SaveEvaluator(UNCHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.has_changes(), new_state.has_changes())

    def test_changed_initial(self):
        old_state = INITIAL

        evaluator = SaveEvaluator(CHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertFalse(new_state.has_changes())

    def test_changed_saved(self):
        old_state = SAVED

        evaluator = SaveEvaluator(CHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertFalse(new_state.has_changes())

    def test_changed_unsaved(self):
        old_state = UNSAVED

        evaluator = SaveEvaluator(CHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertFalse(new_state.has_changes())
