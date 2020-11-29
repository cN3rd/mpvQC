import unittest
from datetime import datetime
from pathlib import Path
from typing import NamedTuple
from unittest.mock import patch

from mpvqc.engine.comment import Comment
from mpvqc.engine.io.document import Document
from mpvqc.engine.io.doc_exporter import DocumentRecipe, DocumentIngredients, DocumentCombiner, Exporter


class MockedSettings(NamedTuple):
    export_write_nickname: bool = True
    export_write_video_path: bool = True
    export_nickname: str = "test-nickname"


class MockedMetadata(NamedTuple):
    app_name: str = "app-name"
    app_version: str = "0.0.7"


class MockedFiles(NamedTuple):
    dir_backup: str = str(Path.home())


class TestData:
    recipe_all = DocumentRecipe(header=True, date=True, generator=True, nick=True, path=True)
    recipe_no_header = DocumentRecipe(header=False, date=True, generator=True, nick=True, path=True)
    recipe_no_nick = DocumentRecipe(header=True, date=True, generator=True, nick=False, path=True)
    recipe_no_path = DocumentRecipe(header=True, date=True, generator=True, nick=True, path=False)

    ingredients = DocumentIngredients(
        date='01.01.1970',
        generator='10km a day',
        nick='saitama',
        path=Path('10 km'),
        comments=(Comment(time="00:00:00", category="ok", comment="ok"),)
    )
    export_path = Path.home()


class TestExporterModule(unittest.TestCase):

    @patch('mpvqc.engine.io.doc_exporter.get_settings', return_value=MockedSettings(export_write_video_path=False))
    def test_document_recipe_from_settings(self, *_):
        recipe = DocumentRecipe.from_settings()
        self.assertTrue(recipe.header, 'Expected document recipe to return True for \'header\'')
        self.assertTrue(recipe.date, 'Expected document recipe to return True for \'date\'')
        self.assertTrue(recipe.generator, 'Expected document recipe to return True for \'generator\'')
        self.assertTrue(recipe.nick, 'Expected document recipe to return True for \'nick\'')
        self.assertFalse(recipe.path, 'Expected document recipe to return False for \'path\'')

    def test_document_recipe_for_backup(self):
        recipe = DocumentRecipe.for_backup()
        self.assertTrue(recipe.header, 'Expected document recipe to return True for \'header\'')
        self.assertTrue(recipe.date, 'Expected document recipe to return True for \'date\'')
        self.assertFalse(recipe.generator, 'Expected document recipe to return False for \'generator\'')
        self.assertFalse(recipe.nick, 'Expected document recipe to return False for \'nick\'')
        self.assertTrue(recipe.path, 'Expected document recipe to return True for \'path\'')

    @patch('mpvqc.engine.io.doc_exporter.get_settings', return_value=MockedSettings(export_nickname='mock-patch'))
    @patch('mpvqc.engine.io.doc_exporter.get_metadata', return_value=MockedMetadata(app_name='mpvKuZeh'))
    def test_document_ingredients_from_document(self, *_):
        video = None
        comments = [
            Comment(time="00:00:00", category="hehe", comment="not like this"),
        ]
        ing = DocumentIngredients.create_from(Document(video, tuple(comments)))
        self.assertIn(str(datetime.now().year), ing.date, 'Year is missing in document ingredients')
        self.assertIn('mpvKuZeh', ing.generator, 'Generator is missing in document ingredients')
        self.assertEqual('mock-patch', ing.nick, 'Nick is wrong in document ingredients')
        self.assertEqual(video, ing.path, 'Path is wrong in document ingredients')
        self.assertEqual(tuple(comments), ing.comments, 'Comments are wrong in document ingredients')

    def test_document_combiner_empty(self):
        doc = DocumentCombiner()
        self.assertFalse(doc.combine(), 'New document without content must be completely empty.')

    def test_document_combiner_write_file_tag(self):
        doc = DocumentCombiner()
        doc.write_file_tag()
        self.assertEqual('[FILE]', doc.combine(), '[FILE] tag missing in newly created document')

    def test_document_combiner_write_complete_header(self):
        path = Path()

        doc = DocumentCombiner()
        doc.write_file_tag()
        doc.write_date('now')
        doc.write_generator('iGenerator')
        doc.write_nick('best-test')
        doc.write_path(path)
        doc = doc.combine()

        lines = doc.splitlines(keepends=False)

        self.assertIn('now', lines[1], 'Date missing in document header')
        self.assertIn('iGenerator', lines[2], 'Generator missing in document header')
        self.assertIn('best-test', lines[3], 'Nick missing in document header')
        self.assertIn(str(path), lines[4], 'Path missing in document header')

    def test_document_combiner_write_two_empty_lines(self):
        doc = DocumentCombiner()
        doc.write_file_tag()
        doc.write_empty_line()
        doc.write_empty_line()
        doc.write_data_tag()
        doc = doc.combine()

        lines = doc.splitlines(keepends=False)
        self.assertEqual(2, len([line for line in lines if not line]),
                         'Document should contain 2 empty lines')

    def test_document_combiner_write_comments(self):
        comments = [
            Comment(time="00:00:00", category="pestilential", comment="please no!"),
            Comment(time="10:00:00", category="covid", comment="please not again!"),
        ]
        doc = DocumentCombiner()
        doc.write_data_tag()
        doc.write_comments(tuple(comments))
        doc = doc.combine()

        for comment in comments:
            self.assertIn(str(comment), doc)

    def test_document_combiner_write_comment_amount(self):
        comments = [
            Comment(time="00:00:00", category="pestilential", comment="please no!"),
            Comment(time="00:00:07", category="covid", comment="please not again!"),
            Comment(time="00:00:00", category="no words", comment=""),
        ]
        doc = DocumentCombiner()
        doc.write_comments(tuple(comments))
        doc.write_comment_summary()
        doc = doc.combine()

        line_summary = doc.splitlines(keepends=False)[-1]
        self.assertTrue(line_summary.split()[-1].isdigit(), 'Comment amount is missing')
        self.assertTrue(line_summary.endswith(f'{len(comments)}'), 'Comment amount is wrong')

    def test_exporter_constructing_from_starts_with_file_tag(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()

        self.assertIn('[FILE]', lines[0],
                      'Created document must begin with the [FILE] tag')

    def test_exporter_constructing_from_writes_date_in_full_header(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()
        self.assertTrue(any(TestData.ingredients.date in line for line in lines),
                        'Date is missing in created document with full header enabled')

    def test_exporter_constructing_from_writes_generator_in_full_header(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()
        self.assertTrue(any(TestData.ingredients.generator in line for line in lines),
                        'Generator is missing in created document with full header enabled')

    def test_exporter_constructing_from_writes_nick_in_full_header(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()
        self.assertTrue(any(TestData.ingredients.nick in line for line in lines),
                        'Nick is missing in created document with full header enabled')

    def test_exporter_constructing_from_writes_path_in_full_header(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()
        self.assertTrue(any(str(TestData.ingredients.path) in line for line in lines),
                        'Path is missing in created document with full header enabled')

    def test_exporter_constructing_from_does_not_write_date_in_no_header(self):
        content = Exporter.construct_from(TestData.recipe_no_header, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(TestData.ingredients.date in line for line in lines),
                         'Date is present in created document with header disabled')

    def test_exporter_constructing_from_does_not_write_generator_in_no_header(self):
        content = Exporter.construct_from(TestData.recipe_no_header, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(TestData.ingredients.generator in line for line in lines),
                         'Generator is present in created document with header disabled')

    def test_exporter_constructing_from_does_not_write_nick_in_no_header(self):
        content = Exporter.construct_from(TestData.recipe_no_header, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(TestData.ingredients.nick in line for line in lines),
                         'Nick is present in created document with header disabled')

    def test_exporter_constructing_from_does_not_write_path_in_no_header(self):
        content = Exporter.construct_from(TestData.recipe_no_header, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(str(TestData.ingredients.path) in line for line in lines),
                         'Path is present in created document with header disabled')

    def test_exporter_constructing_from_does_not_write_nick_in_no_nick(self):
        content = Exporter.construct_from(TestData.recipe_no_nick, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(TestData.ingredients.nick in line for line in lines),
                         'Nick is present in created document even tough it was disabled')

    def test_exporter_constructing_from_does_not_write_path_in_no_path(self):
        content = Exporter.construct_from(TestData.recipe_no_path, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(str(TestData.ingredients.path) in line for line in lines),
                         'Path is present in created document even tough it was disabled')

    def test_exporter_constructing_from_contains_data_tag(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()

        self.assertTrue(any('[DATA]' in line for line in lines))

    def test_exporter_constructing_from_writes_comments(self):
        content = Exporter.construct_from(TestData.recipe_no_path, TestData.ingredients)
        lines = content.splitlines()
        for comment in TestData.ingredients.comments:
            self.assertIn(str(comment), lines)

    def test_exporter_constructing_from_writes_comment_summary(self):
        content = Exporter.construct_from(TestData.recipe_no_path, TestData.ingredients)
        lines = content.splitlines()
        last_content_line = [line for line in lines if line][-1]
        self.assertTrue(last_content_line.split()[-1].isdigit())

    @patch('mpvqc.engine.io.doc_exporter.get_settings', return_value=MockedSettings())
    @patch('mpvqc.engine.io.doc_exporter.get_metadata', return_value=MockedMetadata())
    @patch('mpvqc.engine.io.doc_exporter.Path.write_text')
    def test_exporter_export_calls_file_write_text(self, write_text, *_):
        document = Document(TestData.ingredients.path, comments=TestData.ingredients.comments)
        Exporter.export(document, TestData.export_path)
        write_text.assert_called()

    @patch('mpvqc.engine.io.doc_exporter.get_settings', return_value=MockedSettings())
    @patch('mpvqc.engine.io.doc_exporter.get_metadata', return_value=MockedMetadata())
    @patch('mpvqc.engine.io.doc_exporter.get_files', return_value=MockedFiles())
    @patch('mpvqc.engine.io.doc_exporter.ZipFile')
    def test_exporter_backup_calls_writestr(self, mock_zip, *_):

        class MockedZipFile:
            write_called = False
            close_called = False

            def writestr(self, *_):
                self.write_called = True

            def close(self):
                self.close_called = True

        mocked = MockedZipFile()
        mock_zip.return_value = mocked

        document = Document(TestData.ingredients.path, comments=TestData.ingredients.comments)
        Exporter.backup(document)

        self.assertTrue(mocked.write_called)
        self.assertTrue(mocked.close_called)
