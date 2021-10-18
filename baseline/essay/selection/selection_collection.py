from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import List

from baseline.essay.selection import SelectionAbstract, SelectionFactory


class SelectionIterator(Iterator):
    _position: int = None  # хранит текущее положение обхода

    _reverse: bool = False  # указывает направление обхода

    def __init__(self, collection: List[SelectionAbstract], reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class SelectionCollection(Iterable):

    _collection: List[SelectionAbstract]

    def __init__(self, collection: List[SelectionAbstract] = None) -> None:
        if collection is None:
            collection = []
        self._collection = collection

    def __len__(self) -> int:
        return len(self._collection)

    def __iter__(self) -> List[SelectionAbstract]:
        return self._collection

    def append(self, item: SelectionAbstract):
        self._collection.append(item)

    def get_selections(self) -> List[SelectionAbstract]:
        return self._collection

    def fill(self, selections: List[dict]) -> None:
        for selection_item in selections:
            selection: SelectionAbstract = SelectionFactory.get_instance()
            selection.fill(selection_item)
            self._collection.append(selection)

    def to_list(self) -> List[dict]:
        return list(map(lambda selection: selection.to_dict(), self._collection))


