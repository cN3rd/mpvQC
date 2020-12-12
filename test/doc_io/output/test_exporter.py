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


import unittest
from unittest.mock import patch

from mpvqc.doc_io import Exporter, Document
from test.doc_io.output import TestData, MockedSettings, MockedMetadata, MockedFiles


class TestExporter(unittest.TestCase):

    def test_document_starts_with_file_tag(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()

        self.assertIn('[FILE]', lines[0])

    def test_document_with_header_contains_date(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()
        self.assertTrue(any(TestData.ingredients.date in line for line in lines))

    def test_document_with_header_contains_generator(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()
        self.assertTrue(any(TestData.ingredients.generator in line for line in lines))

    def test_document_with_header_contains_nickname(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()
        self.assertTrue(any(TestData.ingredients.nick in line for line in lines))

    def test_document_with_header_contains_path(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()
        self.assertTrue(any(str(TestData.ingredients.path) in line for line in lines))

    def test_document_without_header_misses_date(self):
        content = Exporter.construct_from(TestData.recipe_no_header, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(TestData.ingredients.date in line for line in lines))

    def test_document_without_header_misses_generator(self):
        content = Exporter.construct_from(TestData.recipe_no_header, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(TestData.ingredients.generator in line for line in lines))

    def test_document_without_header_misses_nick(self):
        content = Exporter.construct_from(TestData.recipe_no_header, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(TestData.ingredients.nick in line for line in lines))

    def test_document_without_header_misses_path(self):
        content = Exporter.construct_from(TestData.recipe_no_header, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(str(TestData.ingredients.path) in line for line in lines))

    def test_document_without_nick_misses_nickname(self):
        content = Exporter.construct_from(TestData.recipe_no_nick, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(TestData.ingredients.nick in line for line in lines))

    def test_document_without_path_misses_path(self):
        content = Exporter.construct_from(TestData.recipe_no_path, TestData.ingredients)
        lines = content.splitlines()
        self.assertFalse(any(str(TestData.ingredients.path) in line for line in lines))

    def test_document_contains_data_tag(self):
        content = Exporter.construct_from(TestData.recipe_all, TestData.ingredients)
        lines = content.splitlines()

        self.assertTrue(any('[DATA]' in line for line in lines))

    def test_document_contains_comments(self):
        content = Exporter.construct_from(TestData.recipe_no_path, TestData.ingredients)
        lines = content.splitlines()
        for comment in TestData.ingredients.comments:
            self.assertIn(str(comment), lines)

    def test_document_ends_with_comments_summary(self):
        content = Exporter.construct_from(TestData.recipe_no_path, TestData.ingredients)
        lines = content.splitlines()
        last_content_line = [line for line in lines if line][-1]
        self.assertTrue(last_content_line.split()[-1].isdigit())

    @patch('mpvqc.doc_io.output.recipe.get_settings', return_value=MockedSettings())
    @patch('mpvqc.doc_io.output.ingredients.get_settings', return_value=MockedSettings())
    @patch('mpvqc.doc_io.output.ingredients.get_metadata', return_value=MockedMetadata())
    @patch('mpvqc.doc_io.output.exporter.Path.write_text')
    def test_export_document_is_written(self, write_text, *_):
        document = Document(TestData.ingredients.path, comments=TestData.ingredients.comments)
        Exporter.export(document, TestData.export_path)
        write_text.assert_called()

    @patch('mpvqc.doc_io.output.recipe.get_settings', return_value=MockedSettings())
    @patch('mpvqc.doc_io.output.ingredients.get_settings', return_value=MockedSettings())
    @patch('mpvqc.doc_io.output.ingredients.get_metadata', return_value=MockedMetadata())
    @patch('mpvqc.doc_io.output.exporter.get_files', return_value=MockedFiles())
    @patch('mpvqc.doc_io.output.exporter.ZipFile')
    def test_export_backup_is_created(self, mock_zip, *_):

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

