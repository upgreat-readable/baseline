from pydantic import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class SessionFileSendDto:
    session_id: int
    file_id: str
    message: Optional[str]
