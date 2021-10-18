from pydantic import dataclasses, Field

from baseline.tools.constants import SessionTypeType, SessionLanguageType, SessionDatasetType


@dataclasses.dataclass(frozen=True)
class SessionStarterOptions:
    type: SessionTypeType = 'algorithmic'

    language: SessionLanguageType = 'rus'
    dataset: SessionDatasetType = 'train'
    file_count: int = Field(300, ge=10, le=1000)
    file_timeout: int = Field(60, ge=10, le=60)

    def prepare_to_command(self) -> dict:
        return {
            'type': self.type,
            'params': {
                'dsType': self.dataset,
                'countFiles': self.file_count,
                'lang': self.language,
                'time': self.file_timeout
            }
        }
