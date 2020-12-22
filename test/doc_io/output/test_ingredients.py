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
from datetime import datetime
from unittest.mock import patch

from mpvqc.doc_io import Document
from mpvqc.doc_io.output.ingredients import DocumentIngredients
from mpvqc.core import Comment
from test.doc_io.input import ANY_PATH
from test.doc_io.output import MockedSettings, MockedMetadata


class TestIngredients(unittest.TestCase):
    GET_SETTINGS = 'mpvqc.doc_io.output.ingredients.get_settings'
    SETTINGS = MockedSettings(export_write_video_path=False)

    GET_METADATA = 'mpvqc.doc_io.output.ingredients.get_metadata'
    METADATA = MockedMetadata(app_name='mpvKuZeh')

    VIDEO = None
    COMMENTS = tuple([Comment(time="00:00:00", category="hehe", comment="not like this")])

    def _get_ingredients(self):
        return DocumentIngredients.create_from(Document(ANY_PATH, self.VIDEO, self.COMMENTS))

    @patch(GET_SETTINGS, return_value=SETTINGS)
    @patch(GET_METADATA, return_value=METADATA)
    def test_date(self, *_):
        ing = self._get_ingredients()
        self.assertIn(str(datetime.now().year), ing.date)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    @patch(GET_METADATA, return_value=METADATA)
    def test_generator(self, *_):
        ing = self._get_ingredients()
        self.assertIn('mpvKuZeh', ing.generator)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    @patch(GET_METADATA, return_value=METADATA)
    def test_nickname(self, *_):
        ing = self._get_ingredients()
        self.assertEqual('test-nickname', ing.nick)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    @patch(GET_METADATA, return_value=METADATA)
    def test_video(self, *_):
        ing = self._get_ingredients()
        self.assertEqual(self.VIDEO, ing.path)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    @patch(GET_METADATA, return_value=METADATA)
    def test_comments(self, *_):
        ing = self._get_ingredients()
        self.assertEqual(tuple(self.COMMENTS), ing.comments)
