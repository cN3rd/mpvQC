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


from mpvqc.core.engine.states.changes_comments import CommentsEvaluator, CommentsChanges
from mpvqc.core.engine.states.state import InitialState, SavedState, UnsavedState
from test.doc_io.input import ANY_PATH, ANY_VIDEO


UNCHANGED = CommentsChanges()
UNCHANGED.changed_comments = False

CHANGED = CommentsChanges()
CHANGED.changed_comments = True

INITIAL = InitialState(video=None, stored_video=None)
SAVED = SavedState(file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple())
UNSAVED = UnsavedState(file=ANY_PATH, video=ANY_VIDEO, stored_video=None, comments=tuple())


class Test(unittest.TestCase):

    def test_no_comments_changes_initial(self):
        old_state = INITIAL

        evaluator = CommentsEvaluator(UNCHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.saved, new_state.saved)

    def test_no_comments_changes_saved(self):
        old_state = SAVED

        evaluator = CommentsEvaluator(UNCHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.saved, new_state.saved)

    def test_no_comments_changes_unsaved(self):
        old_state = UNSAVED

        evaluator = CommentsEvaluator(UNCHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.saved, new_state.saved)

    def test_comments_changes_initial(self):
        old_state = INITIAL

        evaluator = CommentsEvaluator(CHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertNotEqual(old_state.saved, new_state.saved)

    def test_comments_changes_saved(self):
        old_state = SAVED

        evaluator = CommentsEvaluator(CHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertNotEqual(old_state.saved, new_state.saved)

    def test_comments_changes_unsaved(self):
        old_state = UNSAVED

        evaluator = CommentsEvaluator(CHANGED, old_state, comments=tuple())
        new_state = evaluator.evaluate()

        self.assertEqual(old_state.saved, new_state.saved)