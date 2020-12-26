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

from mpvqc.doc_io.output.recipe import DocumentRecipe
from test import MockedSettings


class TestRecipe(unittest.TestCase):
    GET_SETTINGS = 'mpvqc.doc_io.output.recipe.get_settings'
    SETTINGS = MockedSettings(export_write_video_path=False)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    def test_recipe_settings_header(self, *_):
        recipe = DocumentRecipe.from_settings()
        self.assertTrue(recipe.header)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    def test_recipe_settings_date(self, *_):
        recipe = DocumentRecipe.from_settings()
        self.assertTrue(recipe.date)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    def test_recipe_settings_generator(self, *_):
        recipe = DocumentRecipe.from_settings()
        self.assertTrue(recipe.generator)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    def test_recipe_settings_nick(self, *_):
        recipe = DocumentRecipe.from_settings()
        self.assertTrue(recipe.nick)

    @patch(GET_SETTINGS, return_value=SETTINGS)
    def test_recipe_settings_path(self, *_):
        recipe = DocumentRecipe.from_settings()
        self.assertFalse(recipe.path)

    def test_recipe_backup_header(self):
        recipe = DocumentRecipe.for_backup()
        self.assertTrue(recipe.header)

    def test_recipe_backup_date(self):
        recipe = DocumentRecipe.for_backup()
        self.assertTrue(recipe.date)

    def test_recipe_backup_generator(self):
        recipe = DocumentRecipe.for_backup()
        self.assertFalse(recipe.generator)

    def test_recipe_backup_nick(self):
        recipe = DocumentRecipe.for_backup()
        self.assertFalse(recipe.nick)

    def test_recipe_backup_path(self):
        recipe = DocumentRecipe.for_backup()
        self.assertTrue(recipe.path)
