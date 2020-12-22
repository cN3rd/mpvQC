# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

_translate = QCoreApplication.translate


class CheckForUpdates(QMessageBox):
    # todo move into mpvqc.gui.messageboxes

    _UPDATER_URL = "https://mpvqc.rekt.cc/download/latest.txt"

    def __init__(self):
        super().__init__()

        import urllib.request
        import urllib.error

        from mpvqc import get_metadata
        md = get_metadata()

        try:
            r = urllib.request.urlopen(self._UPDATER_URL, timeout=5)
            version_new = r.read().decode("utf-8").strip()
            if md.app_version != version_new:
                self.setWindowTitle(_translate("VersionCheckDialog", "New Version Available"))
                self.setText(
                    _translate("VersionCheckDialog", "There is a new version of mpvQC available ({}).<br>"
                                                     "Visit <a href='https://mpvqc.rekt.cc/'>"
                                                     "https://mpvqc.rekt.cc/</a> to download it.").format(version_new))
                self.setIcon(QMessageBox.Information)
            else:
                self.setWindowTitle("👌")
                self.setText(
                    _translate("VersionCheckDialog", "You are already using the most recent version of mpvQC!"))
                self.setIcon(QMessageBox.Information)
        except urllib.error.HTTPError as e:
            self.setWindowTitle(_translate("VersionCheckDialog", "Server Error"))
            self.setText(_translate("VersionCheckDialog", "The server returned error code {}.").format(e.code))
            self.setIcon(QMessageBox.Warning)
        except urllib.error.URLError:
            self.setWindowTitle(_translate("VersionCheckDialog", "Server Not Reachable"))
            self.setText(_translate("VersionCheckDialog", "A connection to the server could not be established."))
            self.setIcon(QMessageBox.Warning)
