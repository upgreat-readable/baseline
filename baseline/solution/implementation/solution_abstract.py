from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union

from baseline.epicrisis.epicrisis import Epicrisis


class SolutionAbstract(ABC):
    """
    Реализации разметки, имеют 2 метода для асихнронной и синхронной реализации
    """

    @abstractmethod
    async def execute_async(self, epicrisis: Epicrisis) -> list[dict[str, Union[int, str]]]:
        pass

    @abstractmethod
    def execute(self, epicrisis: Epicrisis) -> list[dict[str, Union[int, str]]]:
        pass
