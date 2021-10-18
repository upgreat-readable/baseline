import subprocess

from baseline.calculation.criteria.output_entities import Criteria
from baseline.essay.essay import EssayAbstract, Essay, EssayFactory
from baseline.essay.file import FileAbstract, FileFactory
import json


class CriteriaCalculator:
    result: Criteria
    result_essay_entity: EssayAbstract
    operand_essay_entity: Essay
    path: str

    def enter_operand_by_path(self, path: str):
        try:

            self.path = path
            # @todo неявный выход из директории
            self.operand_essay_entity = EssayFactory.get_instance_from_file('../' + path)
        except Exception as err:
            print('При вводе параметра произошла ошибка.')
            print(err)

    def calculate(self):
        try:
            bashCmd = ["node", "node_modules/@upgreat-readable/criteria/build/bin/criteriacli.js", '-p',
                       self.path]
            process = subprocess.run(bashCmd, capture_output=True)
            output = process.stdout.decode("utf-8")

            correct_json = json.loads(self.operand_essay_entity.to_json())
            criteria_package_result = json.loads(output)
            correct_json['criteria'] = criteria_package_result

            self.result = Criteria(criteria_package_result)
            self.result_essay_entity = EssayFactory.get_instance_psrlike_format_from_dict(correct_json)
        except Exception as err:
            ##@todo логирование
            print('Во время расчёта критериев произошла ошибка.')
            print(err)

    def print_to_stdout(self):
        print('Результат расчёта критериев.')
        print(self.result_essay_entity.to_dict()['criteria'])

    def save_result_in_current_file(self):
        try:
            result_essay_file_bind: FileAbstract = FileFactory.create(self.operand_essay_entity._file._path)
            self.result_essay_entity._file = result_essay_file_bind
            self.result_essay_entity.save()
            print('Файл был успешно пересохранен.')
        except Exception as err:
            print('Во время сохранения файла произошла ошибка.')
            print(err)

    def save_result_in_copy_file(self):
        try:
            path_excluded = str(self.operand_essay_entity._file._path).split('/')
            path_excluded[-1] = path_excluded[-1].replace('.json', '_criteria_result.json')
            copied_file_path = '/'.join(path_excluded)

            copy_essay_file_bind: FileAbstract = FileFactory.create(copied_file_path)
            copy_essay_file_bind.write(self.result_essay_entity.to_json())

            self.result_essay_entity._file = copy_essay_file_bind
            self.result_essay_entity.save()
            print('Файл был успешно скопирован. Новое имя - ' + path_excluded[-1])
        except Exception as err:
            print('Во время копирования файла произошла ошибка!')
            print(err)
