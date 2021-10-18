from pathlib import Path
from typing import Final, Literal
from .env_config import ROOT_DIR, IS_DEBUG, SESSION_IS_ONLY_SAVE_FILES, SESSION_WS_PROTOCOL_VERSION

FILES_DIR: Final[Path] = ROOT_DIR.joinpath('files')
LOGS_DIR: Final[Path] = ROOT_DIR.joinpath('logs')

# types
SessionTypeType: Final = Literal['final', 'algorithmic', 'technical']
SessionLanguageType: Final = Literal['eng', 'rus']
SessionDatasetType: Final = Literal['train', 'test']
