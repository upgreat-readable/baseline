from pydantic import dataclasses, Field

from baseline.tools.constants import SessionContestType, SessionStageType, SessionDatasetType, SessionMainType


@dataclasses.dataclass(frozen=True)
class SessionStarterOptions:
    session_type: SessionMainType = 'training'
    contest: SessionContestType = 'finder'

    stage: SessionStageType = 'rus'
    file_count: int = Field(300, ge=10, le=1000)
    file_timeout: int = Field(60, ge=10, le=60)

    def prepare_to_command(self) -> dict:
        return {
            'contest': self.contest,
            'params': {
                'countFiles': self.file_count,
                'stage': self.stage,
                'sessionType': self.session_type,
                'time': self.file_timeout
            }
        }
