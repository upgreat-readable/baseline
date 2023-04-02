from abc import ABC
from baseline.epicrisis.copy_abstract import CopyAbstract
from baseline.session.dto import input as dto_input
from baseline.epicrisis.file import FileAbstract, FileFactory
from baseline.epicrisis.exceptions import NotHasRequiredFieldError, FileIsExistError, ValidationError


class Epicrisis(CopyAbstract, ABC):
    session_id: int
    epicrisis_id: int
    version_id: int
    team_id: int
    task_id: int
    session_type_code: str
    awsLink: str
    path_to_xml: str
    _file: FileAbstract = None

    def __init__(self, data: dto_input.SessionFileDto):
        self.session_id = data.session_id
        self.epicrisis_id = data.epicrisis_id
        self.version_id = data.version_id
        self.team_id = data.team_id
        self.task_id = data.task_id
        self.session_type_code = data.session_type_code
        self.awsLink = data.aws_link
        self.path_to_xml = f'/sessions/{self.session_id}/{self.epicrisis_id}_{self.version_id}_{self.task_id}.xml'

    @property
    def file(self) -> FileAbstract:
        return self._file

    @file.setter
    def file(self, file: FileAbstract):
        if self._file is not None:
            raise FileIsExistError()
        self._file = file

    def save(self, path: str = None) -> None:
        if self._file is None:
            if path is None:
                raise Exception('File is not exist and path not entered')
        else:
            self._file.write('its work!')

    def copy(self) -> 'Epicrisis':
        return self.__class__._copy(self)

    def __copy__(self) -> 'Epicrisis':
        return self.__class__._copy(self)

    def __deepcopy__(self, memo={}) -> 'Epicrisis':
        return self.__class__._copy(self)

    @classmethod
    def _copy(cls, original: 'Epicrisis') -> 'Epicrisis':
        pass


class EpicrisisFactory:
    @staticmethod
    def get_instance(session_file_event_info: dto_input.SessionFileDto) -> Epicrisis:
        return Epicrisis(session_file_event_info)





