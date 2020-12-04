from pathlib import Path
from typing import Tuple, Optional

from PyQt5.QtWidgets import QWidget

from mpvqc import get_settings
from .open_documents import OpenDocumentsDialog
from .open_network_stream import OpenNetworkStreamDialog
from .open_subtitles import OpenSubtitlesDialog
from .open_video import OpenVideoDialog
from .save import SaveDialog


class AppDialogs:

    @staticmethod
    def import_documents(parent: Optional[QWidget] = None) -> Tuple[Path]:
        s = get_settings()

        d = OpenDocumentsDialog(parent)
        document = s.import_last_dir_document
        d.open(document)

        docs = d.get_documents()
        if docs:
            s.import_last_dir_document = docs[0].parent
        return docs

    @staticmethod
    def import_video(parent: Optional[QWidget] = None) -> Optional[Path]:
        s = get_settings()

        d = OpenVideoDialog(parent)
        d.open(s.import_last_dir_video)

        vid = d.get_video()
        if vid:
            s.import_last_dir_video = vid.parent
        return vid

    @staticmethod
    def import_subtitles(parent: Optional[QWidget] = None) -> Tuple[Path]:
        s = get_settings()

        d = OpenSubtitlesDialog(parent)
        d.open(s.import_last_dir_subtitles)

        subs = d.get_subtitles()
        if subs:
            s.import_last_dir_subtitles = subs[0].parent
        return subs

    @staticmethod
    def export_document(suggested: Optional[Path], parent: Optional[QWidget] = None) -> Path:
        d = SaveDialog(parent)
        d.open(at=suggested)
        return d.get_location()

    @staticmethod
    def import_network_stream(parent: Optional[QWidget] = None) -> Optional[Path]:
        d = OpenNetworkStreamDialog(parent)
        d.open()
        return d.get_path()
