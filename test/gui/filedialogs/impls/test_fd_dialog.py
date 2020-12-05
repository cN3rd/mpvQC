import unittest
from pathlib import Path

from mpvqc.gui.filedialogs.impls import Dialog


class TestDialog(unittest.TestCase):

    def test_home_directory(self, *_):
        dialog = Dialog(parent=None)
        self.assertEqual(str(Path.home()), dialog.home_directory)

    def test_str_to_paths(self):
        path = Path('text-doc.txt')
        path_str = str(path)

        dialog = Dialog(parent=None)
        transformed = dialog.as_paths([path_str])

        self.assertEqual(path.resolve(), transformed[0].resolve())

    def test_str_to_paths_with_spaces_in_normal_paths(self):
        path = Path('/this/is/a/path/with spaces.txt')
        path_str = str(path)

        dialog = Dialog(parent=None)
        transformed = dialog.as_paths([path_str])

        self.assertEqual(path.resolve(), transformed[0].resolve())

    def test_str_to_paths_with_spaces_in_backspace_paths(self):
        path = Path('C:\\this\\is\\a\\path\\with spaces.txt')
        path_str = str(path)

        dialog = Dialog(parent=None)
        transformed = dialog.as_paths([path_str])

        self.assertEqual(path.resolve(), transformed[0].resolve())
