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
from unittest.mock import patch, Mock

from mpvqc.doc_io import Document, Importer
from mpvqc.doc_io.input.error import NotADocumentError
from test.doc_io.input import ANY_PATH, ANY_DOCUMENT, ANY_INCOMPATIBLE


class TestNotADocumentError(unittest.TestCase):
    STR_FILE_READER = 'mpvqc.doc_io.input.importer.FileReader'

    @staticmethod
    def _return(document: Document, on_mock: Mock):
        on_mock.return_value.get_document.return_value = document

    @staticmethod
    def _raise(error: NotADocumentError, on_mock: Mock):
        def _raise_exception():
            raise error
        on_mock.return_value.read.side_effect = _raise_exception

    @patch(STR_FILE_READER)
    def test_document_single(self, m_reader: Mock):
        self._return(ANY_DOCUMENT, on_mock=m_reader)

        importer = Importer(tuple([ANY_PATH]))
        importer.import_them()

        expected = tuple([ANY_DOCUMENT])
        actual = importer.get_import().documents

        self.assertEqual(expected, actual)

    @patch(STR_FILE_READER)
    def test_document_multiple(self, m_reader: Mock):
        self._return(ANY_DOCUMENT, on_mock=m_reader)

        importer = Importer(tuple([ANY_PATH, ANY_PATH]))
        importer.import_them()

        expected = tuple([ANY_DOCUMENT, ANY_DOCUMENT])
        actual = importer.get_import().documents

        self.assertEqual(expected, actual)

    @patch(STR_FILE_READER)
    def test_incompatible_single(self, m_reader: Mock):
        self._raise(NotADocumentError(ANY_PATH), on_mock=m_reader)

        importer = Importer(tuple([ANY_PATH]))
        importer.import_them()

        expected = tuple([ANY_INCOMPATIBLE])
        get_import = importer.get_import()
        actual = get_import.incompatibles

        self.assertEqual(expected, actual)

    @patch(STR_FILE_READER)
    def test_incompatible_multiple(self, m_reader: Mock):
        self._raise(NotADocumentError(ANY_PATH), on_mock=m_reader)

        importer = Importer(tuple([ANY_PATH, ANY_PATH]))
        importer.import_them()

        expected = tuple([ANY_INCOMPATIBLE, ANY_INCOMPATIBLE])
        get_import = importer.get_import()
        actual = get_import.incompatibles

        self.assertEqual(expected, actual)
