from baseline.markup.implementation.markup_abstract import MarkupAbstract
from baseline.markup.implementation.markup_demo import MarkupDemo
from baseline.tools.singleton import MetaSingleton


class MarkupFactory(metaclass=MetaSingleton):
    _markup_implementation: MarkupAbstract

    def __init__(self):
        self.set(MarkupDemo())

    def set(self, markup_implementation: MarkupAbstract):
        self._markup_implementation = markup_implementation

    def get(self) -> MarkupAbstract:
        return self._markup_implementation
