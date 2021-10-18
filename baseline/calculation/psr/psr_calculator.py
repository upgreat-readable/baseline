import os
import subprocess

from baseline.calculation.psr.input_entities import *
from baseline.calculation.psr.output_entities import *
from baseline.essay.essay import EssayFactory
from baseline.calculation.psr.essay_collection import EssayCollection

class PsrCalculator:
    result: ComparisonResultCollection
    operand_essay_collection: list = []

    def enter_operand_by_path(self, path: str):
        #@todo неявный выход из папки
        self.operand_essay_collection.append(EssayFactory.get_instance_psrlike_format_from_file('../'+path))

    def calculate(self):
        try: 
            if len(self.operand_essay_collection) < 2:
                raise Exception('Для создания расчёта необходимо ввести хотя бы две разметки.')

            data_collection = EssayCollection(self.operand_essay_collection)
            psr_operand = PrimitivePsrOperand(data_collection)
            prepared_psr_op = psr_operand.to_json()

            path = 'files/psr_compares/'+data_collection.get_essays()[0].meta.id+'.json'
            file_psr = open(path, "w+")
            file_psr.write(prepared_psr_op)
            file_psr.close()

            bashCmd = ["node", "node_modules/@upgreat-readable/psr/build/bin/psrcli.js", '-p',
                       path]
            process = subprocess.run(bashCmd, capture_output=True)
            output = process.stdout.decode("utf-8")

            raw_calc_result = json.loads(output)
            self.result = ComparisonResultCollection()
            self.result.native_fill_from_dict(raw_calc_result)

            os.remove(path)
        except Exception as err:
            ##@todo логирование
            print('Во время расчёта PSR произошла ошибка.')
            print(err)

    def print_result_to_stdout(self):
        print(self.result.to_json())
        pass






