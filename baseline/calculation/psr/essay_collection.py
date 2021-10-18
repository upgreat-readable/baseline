from typing import List

from baseline.essay.essay import EssayAbstract


class EssayCollection:
    _collection = List[EssayAbstract]

    def __init__(self, collection: List[EssayAbstract] = None) -> None:
        if collection is None:
            collection = []
        self._collection = collection

    def append(self, essay: EssayAbstract):
        self._collection.append(essay)
    
    def get_essays(self):
        return self._collection

class EssayCollectionSupport:
    @staticmethod
    def calcucate_eqality(collection: EssayCollection) -> bool:
        for essay_comparing in collection:
            subject = essay_comparing.meta.subject
            for essay_comparable in collection:
                if subject != essay_comparable.meta.subject:
                    raise ValueError

        return True
