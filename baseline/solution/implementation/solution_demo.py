from abc import ABC
import asyncio
import random
import json
from typing import Union

from loguru import logger

from baseline.tools.env_config import DEBUG_MAX_MARKUP_DEMO_DELAY, CHECK_DIRECTORY_ANSWER, CHECK_DIRECTORY_ANSWER_DELAY

from baseline.solution.implementation.solution_abstract import SolutionAbstract
from baseline.epicrisis.epicrisis import Epicrisis


class SolutionDemo(SolutionAbstract):
    ## Размечаемый эпикриз
    epicrisis: Epicrisis

    xPath: str
    start: int
    end: int
    decorCode: str
    pathToAnswer: str

    _logger = logger

    __DEMO_SOLUTION = {
        'start': 0,
        'end': 1,
        'decorCode': 'diagnosisMain',
        'code': 'X101',
        'name': 'Рак лёгких',
        'xPath': ''
    }

    def __init__(self, epicrisis: Epicrisis):
        self.epicrisis = epicrisis

    async def execute_async(self) -> list[dict[str, Union[int, str]]]:
        await asyncio.sleep(random.randrange(0, DEBUG_MAX_MARKUP_DEMO_DELAY + 1))
        return self.__execute()

    def execute(self) -> list[dict[str, Union[int, str]]]:
        return self.__execute()

    def __execute(self) -> list[dict[str, Union[int, str]]]:
        ## make magic with epicrisis

        self.__DEMO_SOLUTION = [{
            'start': 0,
            'end': 1,
            'decorCode': 'diagnosisMain',
            'code': 'X101',
            'name': 'Рак лёгких',
            'xPath': ''
        }]

        # self.xPath = self.__DEMO_SOLUTION.get('xPath')
        # self.start = self.__DEMO_SOLUTION.get('start')
        # self.end = self.__DEMO_SOLUTION.get('end')
        # self.decorCode = self.__DEMO_SOLUTION.get('decorCode')
        # self.code = self.__DEMO_SOLUTION.get('code')
        # self.name = self.__DEMO_SOLUTION.get('name')
        return self.__DEMO_SOLUTION

    def to_json(self) -> str:
        file_content: dict = {
            'xPath': self.xPath,
            'start': self.start,
            'end': self.end,
            'decorCode': self.decorCode,
            'code': self.code,
            'name': self.name,
        }
        return json.dumps(file_content, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, ensure_ascii=False)




