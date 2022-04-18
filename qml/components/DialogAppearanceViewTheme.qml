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


import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import helpers
import models


ListView {

    id: listViewTheme

    property int itemBorder: 12

    model: ThemeModel {}
    clip: true
    spacing: 8
    height: 52
    orientation: ListView.Horizontal

    delegate: Component {

        Circle {

            width: 52
            height: width
            color: appTheme === theme ? Material.foreground : "transparent"

            Circle {

                width: parent.width - listViewTheme.itemBorder
                height: width
                anchors.centerIn: parent
                color: Material.background

                Material.theme: theme

                onClicked: {
                    appWindow.appTheme = theme
                    MpvqcSettings.theme = theme
                }

            }

        }

    }

}
