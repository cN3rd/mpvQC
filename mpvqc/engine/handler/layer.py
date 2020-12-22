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


from abc import abstractmethod
from typing import TypeVar, Generic


from mpvqc.engine.interface import Options
from mpvqc.engine.states import State, ImportChanges

Response = TypeVar('Response')


class FlowHandler:
    """TOP LAYER"""

    @abstractmethod
    def handle_flow_with(self, options: Options) -> None:
        pass

    @abstractmethod
    def get_changes(self) -> ImportChanges:
        pass


class UserQuestionHandler(Generic[Response]):
    """TOP LAYER"""

    @abstractmethod
    def ask_with(self, current: State, options: Options) -> Response:
        pass


class FlowActions:
    """MIDDLE LAYER"""

    @abstractmethod
    def get_changes(self) -> ImportChanges:
        pass


class FlowQuestion(Generic[Response]):
    """MIDDLE LAYER"""

    @abstractmethod
    def get_the_response(self) -> Response:
        pass
