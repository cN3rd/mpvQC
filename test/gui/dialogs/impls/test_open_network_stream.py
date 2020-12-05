import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from mpvqc.gui.dialogs.impls import OpenNetworkStreamDialog


class TestNetworkStreamDialog(unittest.TestCase):

    @patch('mpvqc.gui.dialogs.impls.open_network_stream.QInputDialog')
    @patch('mpvqc.gui.dialogs.impls.open_documents.QWidget')
    def test_open_passed_in_parent(self, parent: Mock, input_dialog: Mock):
        dialog = OpenNetworkStreamDialog(parent=parent)
        dialog.open()

        input_dialog.assert_called_with(parent)

    @patch('mpvqc.gui.dialogs.impls.open_network_stream.QInputDialog.TextInput')
    @patch('mpvqc.gui.dialogs.impls.open_network_stream.QInputDialog')
    def test_called_set_input_mode(self, input_dialog: Mock, text_input: Mock):
        dialog = OpenNetworkStreamDialog(parent=None)
        dialog.open()

        input_dialog.return_value.setInputMode.assert_called_with(text_input)

    @patch('mpvqc.gui.dialogs.impls.open_network_stream.QInputDialog')
    def test_called_set_window_title(self, input_dialog: Mock):
        dialog = OpenNetworkStreamDialog(parent=None)
        dialog.open()

        title, _ = input_dialog.return_value.setWindowTitle.call_args

        self.assertTrue(title)

    @patch('mpvqc.gui.dialogs.impls.open_network_stream.QInputDialog')
    def test_called_set_label_text(self, input_dialog: Mock):
        dialog = OpenNetworkStreamDialog(parent=None)
        dialog.open()

        title, _ = input_dialog.return_value.setLabelText.call_args

        self.assertTrue(title)

    @patch('mpvqc.gui.dialogs.impls.open_network_stream.QInputDialog')
    def test_called_exec(self, input_dialog: Mock):
        dialog = OpenNetworkStreamDialog(parent=None)
        dialog.open()

        input_dialog.return_value.exec_.assert_called()

    @patch('mpvqc.gui.dialogs.impls.open_network_stream.QInputDialog')
    def test_get_path_on_cancel(self, input_dialog: Mock):
        input_dialog.return_value.textValue.return_value = None

        dialog = OpenNetworkStreamDialog(parent=None)
        dialog.open()
        path = dialog.get_path()

        self.assertFalse(path)

    @patch('mpvqc.gui.dialogs.impls.open_network_stream.QInputDialog')
    def test_get_path_on_success(self, input_dialog: Mock):
        in_path = Path('example')
        input_dialog.return_value.textValue.return_value = in_path

        dialog = OpenNetworkStreamDialog(parent=None)
        dialog.open()
        out_path = dialog.get_path()

        self.assertEqual(out_path.resolve(), in_path.resolve())
