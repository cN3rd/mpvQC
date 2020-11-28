from pathlib import Path
from typing import NamedTuple, Optional, Tuple

from mpvqc.manager_new.comment import Comment


class Document(NamedTuple):
    video: Optional[Path]
    comments: Tuple[Comment]
