from __future__ import annotations

from baseline.epicrisis.epicrisis import Epicrisis
from baseline.essay.essay import EssayAbstract
from baseline.markup.implementation.markup_abstract import MarkupAbstract
from baseline.markup.markup_factory import MarkupFactory
from baseline.tools.singleton import MetaSingleton


class Marker(metaclass=MetaSingleton):
    _markup: MarkupAbstract

    def __init__(self):
        self._markup = MarkupFactory().get()

    async def markup_async(self, epicrisis: Epicrisis) -> EssayAbstract:
        return await self._markup.execute_async(essay=essay)

    def markup(self, essay: EssayAbstract) -> EssayAbstract:
        return self._markup.execute(essay=essay)
