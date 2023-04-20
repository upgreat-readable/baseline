from __future__ import annotations

from baseline.epicrisis.epicrisis import Epicrisis
from baseline.solution.implementation.solution_abstract import SolutionAbstract
from baseline.solution.solution_factory import SolutionFactory
from baseline.tools.singleton import MetaSingleton


class Marker(metaclass=MetaSingleton):
    _solution: SolutionAbstract

    def __init__(self):
        self._solution = SolutionFactory().get()

    async def markup_async(self, epicrisis: Epicrisis) -> str:
        return await self._solution.execute_async(epicrisis)

    def markup(self, epicrisis: Epicrisis) -> str:
        return self._solution.execute(epicrisis)
