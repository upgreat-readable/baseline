from baseline.solution.implementation.solution_abstract import SolutionAbstract
from baseline.solution.implementation.solution_demo import SolutionDemo
from baseline.tools.singleton import MetaSingleton


class SolutionFactory(metaclass=MetaSingleton):
    _solution_implementation: SolutionAbstract

    def __init__(self):
        self.set(SolutionDemo())

    def set(self, solution_implementation: SolutionAbstract):
        self._solution_implementation = solution_implementation

    def get(self) -> SolutionAbstract:
        return self._solution_implementation
