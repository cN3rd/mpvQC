#  mpvQC
#
#  Copyright (C) 2021 mpvQC developers
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

from mpvqc.engine.handler.backup import Backup
from test import MockedSettings
from test.engine import DEFAULT_OPTIONS


class Test(unittest.TestCase):
    MODULE = 'mpvqc.engine.handler.backup'

    GET_SETTINGS = f'{MODULE}.get_settings'

    SETTINGS_10 = MockedSettings(backup_interval=10)
    SETTINGS_60 = MockedSettings(backup_interval=60)

    @patch(GET_SETTINGS, return_value=SETTINGS_10)
    @patch(f'{MODULE}.QTimer.stop')
    def test_reset_timer_stopped(self, mocked_stop: Mock, *_):
        handler = Backup(DEFAULT_OPTIONS)
        handler.reset_timer()
        mocked_stop.assert_called()

    @patch(GET_SETTINGS, return_value=SETTINGS_10)
    @patch(f'{MODULE}.QTimer.start')
    def test_reset_timer_small_interval(self, mocked_start: Mock, *_):
        handler = Backup(DEFAULT_OPTIONS)
        handler.reset_timer()
        mocked_start.assert_not_called()

    @patch(GET_SETTINGS, return_value=SETTINGS_60)
    @patch(f'{MODULE}.QTimer.timeout')
    @patch(f'{MODULE}.QTimer.start')
    def test_reset_timer_big_interval(self, mocked_start: Mock, *_):
        handler = Backup(DEFAULT_OPTIONS)
        handler.reset_timer()
        mocked_start.assert_called()

    @patch(f'{MODULE}.DocumentExporter.backup')
    def test_backup_export_delegated(self, mocked_backup: Mock):
        handler = Backup(DEFAULT_OPTIONS)
        handler.backup()
        mocked_backup.assert_called()

    @patch(f'{MODULE}.DocumentExporter.backup')
    def test_backup_continues_endlessly(self, *_):
        handler = Backup(DEFAULT_OPTIONS)
        continue_further = handler.backup()
        self.assertTrue(continue_further)
