from __future__ import annotations
from abc import ABC, abstractmethod

from baseline.essay.essay import EssayAbstract


class MarkupAbstract(ABC):
    """
    Реализации разметки, имеют 2 метода для асихнронной и синхронной реализации
    """

    @abstractmethod
    async def execute_async(self, essay: EssayAbstract) -> EssayAbstract:
        pass

    @abstractmethod
    def execute(self, essay: EssayAbstract) -> EssayAbstract:
        pass
