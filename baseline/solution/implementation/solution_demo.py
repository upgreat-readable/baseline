from abc import ABC
import asyncio
import random
import json
import os.path
import time

from typing import Union
from pathlib import Path
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
        self._logger.info('execute async runtime')
        self._logger.info(f'env variables - CHECK_DIRECTORY_ANSWER = {CHECK_DIRECTORY_ANSWER}')
        self._logger.info(f'env variables - CHECK_DIRECTORY_ANSWER_DELAY = {CHECK_DIRECTORY_ANSWER_DELAY}')

        directory_conventional_name = f'files/sessions/{self.epicrisis.session_id}/output/{self.epicrisis.epicrisis_id}_{self.epicrisis.version_id}_{self.epicrisis.task_id}.json'


        counter = 0
        while not os.path.exists(directory_conventional_name) | (counter == 60):
            self._logger.info(
                f'while loop')
            time.sleep(1)
            counter += 1

        if os.path.isfile(directory_conventional_name):
            self._logger.info(f'Solution file found. {self.epicrisis.epicrisis_id}_{self.epicrisis.version_id}_{self.epicrisis.task_id}.json')
        else:
            raise ValueError("%s isn't a file!" % directory_conventional_name)



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




