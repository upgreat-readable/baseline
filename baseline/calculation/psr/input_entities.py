from baseline.essay.essay import EssayAbstract
from baseline.essay.meta import MetaAbstract
from baseline.essay.selection.selection import SelectionAbstract
from baseline.essay.criteria import CriteriaAbstract
from baseline.calculation.psr.essay_collection import EssayCollection, EssayCollectionSupport
from typing import List
import json

class ComparedMarkup:
    id: str
    isExpert: bool
    third: bool
    selections: List[SelectionAbstract]
    criteria: CriteriaAbstract

    def fill(self, essay: EssayAbstract):
        self.id = essay._meta.id
        self.isExpert = essay.is_expert
        self.third = False
        self.selections = essay._selections._collection
        self.criteria = essay._criteria


class InputEssayContent:
    id: str
    meta: dict
    text: str
    subject: str
    markups: List[ComparedMarkup]

    def fill(self, essay_collection: EssayCollection):
        #валидация по всей мета на предмет совместимости, как гарант того, что файлы отличаются только селекшнами
        self.id = essay_collection._collection[0].meta.id
        self.meta = essay_collection._collection[0].meta.to_dict()
        self.text = essay_collection._collection[0]._text
        self.subject = essay_collection._collection[0]._text

        self.markups = []

        for essay in essay_collection._collection :
            markup_temp = ComparedMarkup()
            markup_temp.fill(essay)

            self.markups.append(markup_temp)       


class PrimitivePsrOperand:
    essay: InputEssayContent

    def __init__(self, essay_collection: EssayCollection) -> None:
        try:
            EssayCollectionSupport.calcucate_eqality(essay_collection._collection)
        except Exception as err:
            print('Во время расчёта PSR произошла ошибка.')
            print(err)
            # raise Exception('При инициализации произошла ошибка')

        self.fill_from_collection(essay_collection)        

    def fill_from_collection(self, essay_collection: EssayCollection):
        self.essay = InputEssayContent()
        self.essay.fill(essay_collection)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, ensure_ascii=False)

