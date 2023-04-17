from abc import ABC
from baseline.solution.implementation.solution_abstract import SolutionAbstract

class SolutionDemo(SolutionAbstract):
    xPath: str
    start: int
    end: int
    decorCode: str
    pathToAnswer: str

    async def execute_async(self, essay: EssayAbstract) -> EssayAbstract:
        await asyncio.sleep(random.randrange(0, DEBUG_MAX_MARKUP_DEMO_DELAY + 1))
        return self.__execute(essay)

    def execute(self, essay: EssayAbstract) -> EssayAbstract:
        return self.__execute(essay)

    def __execute(self, essay: EssayAbstract) -> EssayAbstract:
        demo_selection = self.__DEMO_SELECTION_BY_SUBJECT.get(essay.meta.subject)

        markup_essay = essay.copy()

        if demo_selection is not None:
            if isinstance(demo_selection, list):
                for item in demo_selection:
                    selection = Selection()
                    selection.fill(item)
                    markup_essay.selections.append(selection)
            elif isinstance(demo_selection, dict):
                selection = Selection()
                selection.fill(demo_selection)
                markup_essay.selections.append(selection)

        return markup_essay

    __DEMO_SELECTION_BY_SUBJECT = {
        'rus': {
            'id': 111,
            'startSelection': 10,
            'endSelection': 20,
            'type': 'П.проблема',
            'comment': '',
            'explanation': '',
            'correction': '',
            'tag': '',
            'group': 'meaning',
            'subtype': '',
        },
        'lit': {
            'id': 111,
            'startSelection': 10,
            'endSelection': 20,
            'type': 'С.опора',
            'comment': '',
            'explanation': '',
            'correction': '',
            'tag': '',
            'group': 'meaning',
            'subtype': '',
        },
        'social': {
            'id': 111,
            'startSelection': 10,
            'endSelection': 20,
            'type': 'о.смысл',
            'comment': '',
            'explanation': '',
            'correction': '',
            'tag': '',
            'group': 'error',
            'subtype': '',
        },
        'rus-free': {
            'id': 111,
            'startSelection': 10,
            'endSelection': 20,
            'type': 'Г.слов',
            'comment': '',
            'explanation': '',
            'correction': '',
            'tag': '',
            'group': 'error',
            'subtype': '',
        },
        'hist': {
            'id': 111,
            'startSelection': 10,
            'endSelection': 20,
            'type': 'И.личность',
            'comment': '',
            'explanation': '',
            'correction': '',
            'tag': '',
            'group': 'error',
            'subtype': '',
        },
        'eng': {
            'id': 111,
            'startSelection': 10,
            'endSelection': 20,
            'type': 'А.стиль',
            'comment': '',
            'explanation': '',
            'correction': '',
            'tag': '',
            'group': 'error',
            'subtype': '',
        },
        'eng-free': {
            'id': 111,
            'startSelection': 10,
            'endSelection': 20,
            'type': 'А.стиль',
            'comment': '',
            'explanation': '',
            'correction': '',
            'tag': '',
            'group': 'error',
            'subtype': '',
        },
    }


