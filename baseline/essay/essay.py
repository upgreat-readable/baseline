from abc import ABC
import json
from pathlib import Path

from baseline.essay.copy_abstract import CopyAbstract
from baseline.essay.selection import SelectionCollection
from baseline.essay.meta import MetaAbstract, MetaFactory
from baseline.essay.file import FileAbstract, FileFactory
from baseline.essay.exceptions import NotHasRequiredFieldError, FileIsExistError, ValidationError
from baseline.essay.validator.validator import EssayValidator
from baseline.essay.criteria import CriteriaAbstract, CriteriaFactory


class EssayAbstract(CopyAbstract, ABC):
    _text: str

    _meta: MetaAbstract

    _selections: SelectionCollection

    _file: FileAbstract = None

    _validator: EssayValidator

    def __init__(self, text: str, meta: MetaAbstract, selection: SelectionCollection = None):
        if not isinstance(meta, MetaAbstract):
            raise ValueError('Argument "meta" should be MetaAbstract object')

        if len(str(text)) == 0:
            raise ValueError('Argument "text" should not be empty')

        self._text = str(text)
        self._meta = meta

        if selection is None:
            selection = SelectionCollection()
        self._selections = selection

        self._validator = EssayValidator(self)

    @classmethod
    def load(cls, data: dict, validate: bool = False) -> 'EssayAbstract':
        if validate is True:
            EssayValidator.validate_essay(data)

        has_required_field = 'text' in data and 'meta' in data
        if not has_required_field:
            raise NotHasRequiredFieldError('Field "text" or "meta" not in json object')

        meta = MetaFactory.get_instance()
        meta.fill(data['meta'])

        selections = SelectionCollection()
        if 'selections' in data and len(data['selections']) > 0:
            selections.fill(data['selections'])

        return cls(data['text'], meta, selections)

    @property
    def text(self) -> str:
        return self._text

    @property
    def is_expert(self) -> bool:
        return len(self._meta.expert) > 0

    @property
    def meta(self) -> MetaAbstract:
        return self._meta

    @property
    def selections(self) -> SelectionCollection:
        return self._selections

    @selections.setter
    def selections(self, selections: SelectionCollection) -> None:
        self._selections = selections

    @property
    def file(self) -> FileAbstract:
        return self._file

    @file.setter
    def file(self, file: FileAbstract):
        if self._file is not None:
            raise FileIsExistError()
        self._file = file

    # @file.deleter for delete file in fs

    @staticmethod
    def parse_json(json_value: str) -> dict:
        content: dict = json.loads(json_value)
        return content

    def to_json(self) -> str:
        file_content: dict = {
            'text': self._text,
            'meta': self._meta.to_dict(),
        }
        if len(self._selections) > 0:
            file_content['selections'] = self._selections.to_list()

        return json.dumps(file_content, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, ensure_ascii=False)

    def to_dict(self) -> dict:
        file_content: dict = {
            'text': self._text,
            'meta': self._meta.to_dict(),
        }
        if len(self._selections) > 0:
            file_content['selections'] = self._selections.to_list()

        return file_content

    def save(self, path: str = None) -> None:
        if self._file is None:
            if path is None:
                raise Exception('File is not exist and path not entered')
        else:
            self._file.write(self.to_json())

    def validate(self):
        is_valid = self._validator.is_valid()

        if not is_valid:
            raise ValidationError(self._validator.get_errors())

    def copy(self) -> 'EssayAbstract':
        return self.__class__._copy(self)

    def __copy__(self) -> 'EssayAbstract':
        return self.__class__._copy(self)

    def __deepcopy__(self, memo={}) -> 'EssayAbstract':
        return self.__class__._copy(self)

    @classmethod
    def _copy(cls, original: 'EssayAbstract') -> 'EssayAbstract':
        pass


class Essay(EssayAbstract):
    @classmethod
    def _copy(cls, original: 'EssayAbstract') -> 'Essay':
        # @todo сделать метод copy для meta.copy()
        return cls(text=original.text, meta=original.meta)


class EssayWithCriteria(Essay):
    _criteria: CriteriaAbstract

    def __init__(self, text: str, meta: MetaAbstract, selection: SelectionCollection = None, criteria: CriteriaAbstract = None):
        self._criteria = criteria
        super().__init__(text=text, meta=meta, selection=selection)

    @property
    def criteria(self) -> CriteriaAbstract:
        return self._criteria

    def to_json(self) -> str:
        file_content: dict = {
            'text': self._text,
            'meta': self._meta.to_dict(),
            'criteria': self._criteria.to_dict(),
            'selections': self._selections.to_list()
        }
        return json.dumps(file_content, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, ensure_ascii=False)

    def to_dict(self) -> dict:
        file_content: dict = {
            'text': self._text,
            'meta': self._meta.to_dict(),
            'criteria': self._criteria.to_dict(),
            'selections': self._selections.to_list()
        }
        return file_content

    @classmethod
    def load(cls, data: dict, validate: bool = False) -> 'EssayAbstract':
        if validate is True:
            EssayValidator.validate_essay(data)

        has_required_field = 'text' in data and 'meta' in data
        if not has_required_field:
            raise NotHasRequiredFieldError('Field "text" or "meta" not in json object')

        meta = MetaFactory.get_instance()
        meta.fill(data['meta'])

        criteria = CriteriaFactory.get_instance()
        #@todo проверку мб вынести в отдельный метод
        if not data['criteria']:
            #@todo посмотреть в сторону деструкторов
            criteria_values = {'K1': 0, 'K2': 0, 'K3': 0, 'K4': 0, 'K5': 0, 'K6': 0, 'K7': 0, 'K8': 0, 'K9': 0, 'K10': 0, 'K11': 0, 'K12': 0}
        else: 
            criteria_values = data['criteria']

        criteria.fill(criteria_values)
        selections = SelectionCollection()
        if 'selections' in data and len(data['selections']) > 0:
            selections.fill(data['selections'])

        return cls(data['text'], meta, selections, criteria)

    @classmethod
    def _copy(cls, original: 'EssayAbstract'):
        pass


class EssayFactory:
    @staticmethod
    def get_instance(text: str, meta: MetaAbstract, selection: SelectionCollection = None) -> EssayAbstract:
        return Essay(text, meta, selection)

    @staticmethod
    def get_instance_from_dict(json_value: dict, validate: bool = False) -> EssayAbstract:
        return Essay.load(json_value, validate=validate)

    @staticmethod
    def get_instance_from_json(json_value: str, validate: bool = False) -> EssayAbstract:
        content: dict = EssayAbstract.parse_json(json_value)
        return Essay.load(content, validate=validate)

    @staticmethod
    def get_instance_from_file(path: str, validate: bool = False) -> EssayAbstract:
        user_path = Path(path)

        file: FileAbstract = FileFactory.create(user_path)
        json_value = file.read()
        content: dict = EssayAbstract.parse_json(json_value)
        essay = Essay.load(content, validate=validate)
        essay.file = file
        return essay

    @staticmethod
    def get_instance_psrlike_format_from_file(path: str, validate: bool = False) -> EssayAbstract:
        # @todo по факту тут возвращается конкретный класс эссе, надо указать EssayForPsr
        # @todo в EssayForPsr.load тоже нужно указать что возвращается EssayForPsr
        user_path = Path(path)

        file: FileAbstract = FileFactory.create(user_path)
        json_value = file.read()
        content: dict = EssayWithCriteria.parse_json(json_value)
        essay = EssayWithCriteria.load(content, validate=validate)
        essay.file = file
        return essay

    @staticmethod
    def get_instance_psrlike_format_from_dict(json_value: dict, validate: bool = False) -> EssayAbstract:
        return EssayWithCriteria.load(json_value, validate=validate)

    @staticmethod
    def get_instance_psrlike_format_from_json(json_value: str, validate: bool = False) -> EssayAbstract:
        content: dict = EssayAbstract.parse_json(json_value)
        return EssayWithCriteria.load(content, validate=validate)


if __name__ == '__main__':
    essay_obj = EssayFactory.get_instance_from_file(path='custom/test.json')
    print(essay_obj.meta.to_dict())
    print(essay_obj.to_json())

    essay_obj.validate()
