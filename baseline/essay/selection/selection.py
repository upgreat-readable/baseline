from abc import ABC
from typing import Literal

SelectionGroupType = Literal['error', 'meaning']
SELECTION_GROUP_TYPE = ['error', 'meaning']


class SelectionAbstract(ABC):
    id: int
    startSelection: int
    endSelection: int
    type: str
    comment: str
    explanation: str
    correction: str
    tag: str
    group: SelectionGroupType
    subtype: str

    def __init__(self, selection: dict = None):
        if selection is not None:
            self.fill(selection)

    def fill(self, selection: dict) -> None:
        self.id = selection.get('id')
        self.startSelection = int(selection.get('startSelection'))
        self.endSelection = int(selection.get('endSelection'))
        self.type = selection.get('type')
        self.comment = selection.get('comment') or ''
        self.explanation = selection.get('explanation') or ''
        self.correction = selection.get('correction') or ''
        self.tag = selection.get('tag') or ''
        self.group = selection.get('group')
        self.subtype = selection.get('subtype') or ''

        self.validate()

    def to_dict(self) -> dict:
        return self.__dict__

    def validate(self) -> bool:
        if self.type is None or len(self.type) == 0:
            raise ValueError('Field "type" in selection required')

        if self.startSelection is None or self.startSelection < 0:
            raise ValueError('Field "startSelection" in selection required and should be great or equal 0')

        if self.endSelection is None or self.startSelection < 0:
            raise ValueError('Field "endSelection" in selection required and should be great or equal 0')

        if self.startSelection > self.endSelection:
            raise ValueError('Field "startSelection" should be less or equal the "endSelection" field')

        if self.group not in SELECTION_GROUP_TYPE:
            raise ValueError(f'Field "group" should be include in [{",".join(SELECTION_GROUP_TYPE)}]')

        return True


class Selection(SelectionAbstract):
    pass


class SelectionFactory:
    @staticmethod
    def get_instance() -> SelectionAbstract:
        return Selection()
