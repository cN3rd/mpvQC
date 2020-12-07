from typing import Optional

from PyQt5.QtWidgets import QWidget


class MessageBox:

    def __init__(self, parent: Optional[QWidget] = None):
        self._parent = parent
