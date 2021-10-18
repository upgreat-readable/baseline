from pydantic import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class SessionFileDto:
    session_id: Optional[int]
    file_id: str
    content: dict
