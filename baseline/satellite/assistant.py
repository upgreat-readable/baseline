import json

from abc import ABC
from baseline.essay.essay import EssayFactory
from baseline.essay.essay import EssayAbstract
from baseline.essay.file import FileAbstract, FileFactory
from pathlib import Path
from typing import Any
from baseline.satellite.archiver import get_essays_list


class Blank:
    id: str
    answer: Any

    def fill(self, blank: dict):
        self.id = blank["id"]
        self.answer = blank["answer"]


class Assistant(ABC):
    essay: EssayAbstract
    mode: str
    stage: str
    operand_path: str
    blank: Blank

    def get_essay(self, essay_id: str, mode: str, stage: str):
        self.operand_path = 'satellite/'+mode+'/'
        self.essay = EssayFactory.get_instance_from_file(self.operand_path+'essays/'+essay_id)
        self.mode = mode
        self.stage = stage
        self.blank = Blank()

        pass

    def get_blank_for_essay(self):
        if self.mode in ['test', 'final']:
            blank_file = FileFactory.create(Path(self.operand_path + self.stage + '_task.json'))
            json_file = json.loads(blank_file.read())

            for blank in json_file:
                if blank["id"] == self.essay.meta.id:
                    self.blank.fill(blank)
        else:
            raise Exception('Данный метод доступен только для датасета, который поставляется с файлом задания ('
                            'test/final).')
        pass

    def set_answer(self, answer: Any):
        self.blank.answer = answer

    def save_answer_for_essay(self):
        if self.mode in ['test', 'final']:
            blank_file = FileFactory.create(Path(self.operand_path + self.stage + '_task.json'))
            json_file = json.loads(blank_file.read())
            for blank in json_file:
                if blank["id"] == self.essay.meta.id:
                    blank["answer"] = self.blank.answer

            blank_file.write(json.dumps(json_file))
        else:
            raise Exception('Данный метод доступен только для датасета, который поставляется с файлом задания ('
                            'test/final).')

        pass

    def check_the_solution(self):
        if self.mode == 'train':
            blank_file = FileFactory.create(Path(self.operand_path + self.stage + '_standart.json'))
            json_file = json.loads(blank_file.read())
            for blank in json_file:
                if blank["id"] == self.essay.meta.id:
                    if blank["answer"] == self.blank.answer:
                        print(self.essay.meta.id + ' correct')
                    else:
                        raise Exception(self.essay.meta.id + ' incorrect')
        else:
            raise Exception('Файл стандарт поставляется только в тренировочном архиве.')







