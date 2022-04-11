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


MouseArea {

    property int borderWidth

    hoverEnabled: true
    acceptedButtons: Qt.NoButton // don't actually handle events

    cursorShape: {
        const p = Qt.point(mouseX, mouseY)
        const b = borderWidth + 15 // Increase the corner size slightly
        if (p.x < b && p.y < b) return Qt.SizeFDiagCursor
        if (p.x >= width - b && p.y >= height - b) return Qt.SizeFDiagCursor
        if (p.x >= width - b && p.y < b) return Qt.SizeBDiagCursor
        if (p.x < b && p.y >= height - b) return Qt.SizeBDiagCursor
        if (p.x < b || p.x >= width - b) return Qt.SizeHorCursor
        if (p.y < b || p.y >= height - b) return Qt.SizeVerCursor
    }

}
