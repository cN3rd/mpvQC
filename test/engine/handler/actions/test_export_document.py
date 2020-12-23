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

from mpvqc.engine.handler.actions import DocumentExporter
from test.doc_io.input import ANY_DOCUMENT


class TestExportDocument(unittest.TestCase):
    EXPORT = 'mpvqc.doc_io.Exporter.export'
    BACKUP = 'mpvqc.doc_io.Exporter.backup'

    @patch(EXPORT)
    def test_export(self, export_func: Mock):
        DocumentExporter.export(ANY_DOCUMENT)
        export_func.assert_called_once()

    @patch(BACKUP)
    def test_backup(self, backup_func: Mock):
        DocumentExporter.backup(ANY_DOCUMENT)
        backup_func.assert_called_once()
