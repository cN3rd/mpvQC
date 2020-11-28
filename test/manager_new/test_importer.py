import unittest
from pathlib import Path
from unittest import SkipTest
from unittest.mock import patch, mock_open

from mpvqc.manager_new.importer import Importer
from mpvqc.manager_new.document import Document


def ensure_result(result: Document):
    if result is None:
        raise SkipTest('Precondition not met: result is None')


def ensure_has_video(result: Document):
    ensure_result(result)
    if result.video is None:
        raise SkipTest('Precondition not met: video is None')


def ensure_has_comments(result: Document):
    ensure_result(result)
    if result.comments is None:
        raise SkipTest('Precondition not met: \'comments\' is None')


class TestImporter(unittest.TestCase):
    PATH = Path()
    IMPORTER = Importer()

    def _read(self, feed: str) -> Document:
        with patch('pathlib.Path.open', mock_open(read_data=feed)):
            with self.PATH.open():
                # print(f.read())
                return self.IMPORTER.import_this(self.PATH)

    def test_importer_does_not_return_none_on_invalid_file(self):
        content = ''
        result = self._read(content)
        self.assertIsNotNone(result, 'Importer must not return None on invalid file')

    def test_importer_does_not_return_none_on_valid_file(self):
        content = '[FILE]'
        result = self._read(content)
        self.assertIsNotNone(result, 'Importer must not return None on valid file')

    def test_importer_returns_comments_tuple_on_invalid_file(self):
        content = ''

        result = self._read(content)
        ensure_result(result)

        self.assertTrue(isinstance(result.comments, tuple), 'Importer must return a tuple with comments')

    def test_importer_returns_comments_tuple_on_valid_file_with_comments(self):
        content = \
            ('[FILE]\n'
             '\n'
             '[DATA]\n'
             '[00:00:00] [Translation] this is wrong\n'
             '[00:10:10] [Translation] this is wrong, too\n'
             '[00:19:10] [Spelling] better\n')
        result = self._read(content)
        ensure_result(result)

        self.assertTrue(isinstance(result.comments, tuple), 'Importer must return a tuple with comments')

    def test_importer_returns_comments_tuple_on_valid_file_without_comments(self):
        content = '[FILE]'

        result = self._read(content)
        ensure_result(result)

        self.assertTrue(isinstance(result.comments, tuple), 'Importer must return a tuple with comments')

    def test_importer_returns_video_path_object_on_invalid_file(self):
        content = ''

        result = self._read(content)
        ensure_result(result)

        self.assertTrue(isinstance(result.video, Path), 'Importer must return a path object')

    def test_importer_returns_video_path_object_on_valid_file_with_path(self):
        video = '/file/path/of/video'
        content = \
            '[FILE]\n' \
            f'path : {video}\n'

        result = self._read(content)
        ensure_result(result)

        self.assertTrue(isinstance(result.video, Path), 'Importer must return a path object')

    def test_importer_returns_video_path_object_on_valid_file_without_path(self):
        content = '[FILE]'

        result = self._read(content)
        ensure_result(result)

        self.assertTrue(isinstance(result.video, Path), 'Importer must return a path object')

    def test_importer_parses_video_path_squished(self):
        video = '/file/path/of/video'
        content = \
            '[FILE]\n' \
            f'path:{video}\n'

        result = self._read(content)
        ensure_has_video(result)

        self.assertEqual(video, str(result.video),
                         'Importer failed to parse the video path when the path followed a colon immediately')

    def test_importer_parses_video_path_with_space_on_both_sides_of_colon(self):
        video = '/file/path/of/video'
        content = \
            '[FILE]\n' \
            f'path  :  {video}\n'

        result = self._read(content)
        ensure_has_video(result)

        self.assertEqual(video, str(result.video),
                         'Importer failed to parse the video path when there was space '
                         'between \'path\', colon and video path')

    def test_importer_parses_video_path_with_space_before_colon(self):
        video = '/file/path/of/video'
        content = \
            '[FILE]\n' \
            f'path  :{video}\n'

        result = self._read(content)
        ensure_has_video(result)

        self.assertEqual(video, str(result.video),
                         'Importer failed to parse the video path when there was space between \'path\' and colon')

    def test_importer_parses_video_path_with_space_after_colon(self):
        video = '/file/path/of/video'
        content = \
            '[FILE]\n' \
            f'path:  {video}\n'

        result = self._read(content)
        ensure_has_video(result)

        self.assertEqual(video, str(result.video),
                         'Importer failed to parse the video path when there was space between colon and video path')

    def test_importer_parses_video_path_on_full_header_at_the_top(self):
        video = '/file/path/of/video'
        content = \
            ('[FILE]\n'
             f'path      : {video}\n'
             f'date      : 2020-09-23 13:09:58\n'
             f'generator : mpvQC 0.7.0\n'
             f'nickname  : nick\n')

        result = self._read(content)
        ensure_has_video(result)

        self.assertEqual(video, str(result.video),
                         'Importer failed to parse the video path on a full header '
                         'when the path was located at the top')

    def test_importer_parses_video_path_on_full_header_at_the_center(self):
        video = '/file/path/of/video'
        content = \
            ('[FILE]\n'
             f'date      : 2020-09-23 13:09:58\n'
             f'path      : {video}\n'
             f'generator : mpvQC 0.7.0\n'
             f'nickname  : nick\n')

        result = self._read(content)
        ensure_has_video(result)

        self.assertEqual(video, str(result.video),
                         'Importer failed to parse the video path on a full header '
                         'when the path was located at the center')

    def test_importer_parses_video_path_on_full_header_at_the_bottom(self):
        video = '/file/path/of/video'
        content = \
            ('[FILE]\n'
             f'date      : 2020-09-23 13:09:58\n'
             f'generator : mpvQC 0.7.0\n'
             f'nickname  : nick\n'
             f'path      : {video}\n')

        result = self._read(content)
        ensure_has_video(result)

        self.assertEqual(video, str(result.video),
                         'Importer failed to parse the video path on a full header '
                         'when the path was located at the bottom')

    def test_importer_parses_0_comments(self):
        content = \
            ('[FILE]\n'
             '\n'
             '[DATA]\n')

        result = self._read(content)
        ensure_has_comments(result)

        self.assertEqual(0, len(result.comments), 'Importer must not find any comments when there are no comments')

    def test_importer_parses_1_comment(self):
        content = \
            ('[FILE]\n'
             '\n'
             '[DATA]\n'
             '[00:00:00] [Translation] this is wrong\n')

        result = self._read(content)
        ensure_has_comments(result)

        self.assertEqual(1, len(result.comments),
                         'Importer must find only one comment when there are is only one comment')

    def test_importer_parses_multiple_comments(self):
        content = \
            ('[FILE]\n'
             '\n'
             '[DATA]\n'
             '[00:00:00] [Translation] this is wrong\n'
             '[00:10:10] [Translation] this is wrong, too\n'
             '[00:19:10] [Spelling] better\n')

        result = self._read(content)
        ensure_has_comments(result)

        self.assertEqual(3, len(result.comments),
                         'Importer must find three comments when there are three comments')

    def test_importer_parses_comments_with_space_between_time_and_type(self):
        flawed__ = '[00:00:00][Translation] this is wrong\n'
        self._ensure_flawed_comment_gets_parsed(flawed__,
                                                'Importer must parse comment even when '
                                                'there is no space between time and type')

    def test_importer_parses_comments_with_space_between_type_and_note(self):
        flawed__ = '[00:00:00] [Translation]this is wrong\n'
        self._ensure_flawed_comment_gets_parsed(flawed__,
                                                'Importer must parse comment even when '
                                                'there is no space between type and note')

    def test_importer_parses_comments_with_space_after_note(self):
        flawed__ = '[00:00:00] [Translation] this is wrong   \r\n'
        self._ensure_flawed_comment_gets_parsed(flawed__,
                                                'Importer must parse comment even when '
                                                'there is space after the note')

    def test_importer_parses_comments_without_note(self):
        flawed__ = '[00:00:00] [Translation]\n'
        self._ensure_flawed_comment_gets_parsed(flawed__, 'Importer must parse comment even when note is empty')

    def _ensure_flawed_comment_gets_parsed(self, flawed, message):
        content = \
            ('[FILE]\n'
             '\n'
             '[DATA]\n'
             f'{flawed}')

        result = self._read(content)
        ensure_has_comments(result)

        self.assertTrue(result.comments, message)
        self.assertEqual(1, len(result.comments), message)

    def test_importer_parses_comment_time_successfully(self):
        expected = '00:00:00'
        content = \
            ('[FILE]\n'
             '\n'
             '[DATA]\n'
             f'[{expected}] [Translation] this is wrong\n')

        result = self._read(content)
        ensure_has_comments(result)

        self.assertEqual(expected, result.comments[0].comment_time, 'Importer must parse the time correctly')

    def test_importer_parses_comment_type_successfully(self):
        expected = 'Translation'
        self._ensure_comment_type_matches(expected, type_input='Translation')
        self._ensure_comment_type_matches(expected, type_input='  Translation')
        self._ensure_comment_type_matches(expected, type_input='Translation  ')

    def _ensure_comment_type_matches(self, expected, type_input):
        content = \
            ('[FILE]\n'
             '\n'
             '[DATA]\n'
             f'[00:00:00] [{type_input}] this is wrong\n')

        result = self._read(content)
        ensure_has_comments(result)

        self.assertEqual(expected, result.comments[0].comment_type, 'Importer must parse the type correctly')

    def test_importer_parses_comment_note_successfully(self):
        self._ensure_comment_note_matches(expected='', note_input='')
        self._ensure_comment_note_matches(expected='', note_input='   ')
        self._ensure_comment_note_matches(expected='', note_input='   \r\t\n')
        self._ensure_comment_note_matches(expected='This is my comment', note_input='This is my comment')
        self._ensure_comment_note_matches(expected='This is my comment', note_input='  This is my comment')
        self._ensure_comment_note_matches(expected='This is my comment', note_input='This is my comment  ')

    def _ensure_comment_note_matches(self, expected, note_input):
        content = \
            ('[FILE]\n'
             '\n'
             '[DATA]\n'
             f'[00:00:00] [Translation] {note_input}\n')

        result = self._read(content)
        ensure_has_comments(result)

        self.assertEqual(expected, result.comments[0].comment_note, 'Importer must parse the note correctly')
