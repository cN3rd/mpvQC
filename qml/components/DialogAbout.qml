/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick.Controls
import QtQuick.Layouts


Dialog {
    width: 420
    height: 500

    modal: true
    anchors.centerIn: parent
    standardButtons: Dialog.Ok
    closePolicy: Popup.CloseOnEscape

    contentItem: ColumnLayout {
        width: parent.width

        TabBar {
            id: bar
            contentWidth: parent.width

            TabButton {
                text: qsTranslate("AboutDialog", "About")
            }

            TabButton {
                text: qsTranslate("AboutDialog", "Credits")
            }
        }

        StackLayout {
            currentIndex: bar.currentIndex
            width: parent.width

            DialogAboutViewAbout { }

            DialogAboutViewCredits { }
        }
    }
}