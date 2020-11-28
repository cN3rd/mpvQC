import unittest

from mpvqc.manager_new.comment import Comment


class TestComment(unittest.TestCase):

    def test_comment_with_same_content_is_same_comment(self):
        comment_1 = Comment('00:00:01', 'Spelling', 'Gotcha!')
        comment_2 = Comment('00:00:01', 'Spelling', 'Gotcha!')

        self.assertEqual(comment_1, comment_2, 'Comment with same content must be considered equal')

    def test_comment_with_different_time_is_different_comment(self):
        comment_1 = Comment('00:00:00', 'Punctuation', 'Gotcha!')
        comment_2 = Comment('00:00:01', 'Punctuation', 'Gotcha!')

        self.assertNotEqual(comment_1, comment_2, 'Comments have different time but are considered equal')

    def test_comment_with_different_category_is_different_comment(self):
        comment_1 = Comment('00:00:01', 'Spelling', 'Gotcha!')
        comment_2 = Comment('00:00:01', 'Punctuation', 'Gotcha!')

        self.assertNotEqual(comment_1, comment_2, 'Comments have different category but are considered equal')

    def test_comment_with_different_note_is_different_comment(self):
        comment_1 = Comment('00:00:00', 'Punctuation', 'Gotcha!')
        comment_2 = Comment('00:00:00', 'Punctuation', 'Gotcha this time!')

        self.assertNotEqual(comment_1, comment_2, 'Comments have different note but are considered equal')

    def test_comments_are_sortable_by_time(self):
        comment_1 = Comment('00:00:01', 'Punctuation', 'Gotcha!')
        comment_2 = Comment('00:00:00', 'Punctuation', 'Gotcha this time!')

        unsorted = [comment_1, comment_2]
        sorted_ = sorted(unsorted)
        smaller_expected = comment_2
        smaller_actual = sorted_[0]

        self.assertEqual(smaller_expected, smaller_actual, 'Comments must be sortable by time')

    def test_comments_are_sortable_by_time_then_by_type(self):
        comment_1 = Comment('00:00:00', 'A', 'Gotcha!')
        comment_2 = Comment('00:00:00', 'B', 'Gotcha this time!')

        unsorted = [comment_2, comment_1]
        sorted_ = sorted(unsorted)
        smaller_expected = comment_1
        smaller_actual = sorted_[0]

        self.assertEqual(smaller_expected, smaller_actual, 'Comments must be sortable by comment type')

    def test_comments_are_sortable_by_time_then_by_type_then_by_note(self):
        comment_1 = Comment('00:00:00', 'Punctuation', 'A')
        comment_2 = Comment('00:00:00', 'Punctuation', 'B')

        unsorted = [comment_2, comment_1]
        sorted_ = sorted(unsorted)
        smaller_expected = comment_1
        smaller_actual = sorted_[0]

        self.assertEqual(smaller_expected, smaller_actual, 'Comments must be sortable by comment note')

    def test_comments_as_string_have_space_between_time_and_type(self):
        comment = Comment('00:00:00', 'Punctuation', 'Gotcha! Gotcha again!')

        string = str(comment)

        self.assertIn('[00:00:00] [Punctuation]', string, 'Comment as string must separate time and type by space')

    def test_comments_as_string_have_space_between_type_and_note(self):
        comment = Comment('00:00:00', 'Punctuation', 'Gotcha! Gotcha again!')

        string = str(comment)

        self.assertIn('[Punctuation] Gotcha! Gotcha again!', string,
                      'Comment as string must separate type and note by space')

    def test_comments_are_stripped_from_whitespace(self):
        comment = Comment('00:00:00', 'Punctuation', 'Gotcha! Gotcha again! ')

        comment = str(comment)
        comment_rstrip = comment.strip()

        self.assertEqual(len(comment), len(comment_rstrip), 'Comments as string must be stripped from whitespace')

    def test_comment_repr_is_a_shorter_variant_than_comment_str(self):
        comment = Comment('00:00:00', 'Punctuation', 'Gotcha! Gotcha again!')

        string = str(comment)
        representation = comment.__repr__()

        self.assertTrue(string.startswith(representation), 'Comments python internal representation must begin '
                                                           'like the string representation')

    def test_comment_input_parameter_whitespace_does_not_matter(self):
        comment_flawed_ = Comment(' 00:00:00 ', ' Punctuation', 'Gotcha!                 \n')
        comment_correct = Comment(' 00:00:00  ', 'Punctuation ', '   Gotcha!')

        self.assertEqual(comment_correct, comment_flawed_, 'Comments must be considered equal')
