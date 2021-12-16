import random
import subprocess

import click
import os.path
from typing import Tuple
from pathlib import Path
from loguru import logger

from baseline.tools.constants import SessionTypeType, SessionLanguageType, SessionDatasetType
from baseline.tools.run import asyncio_run
from baseline.session.dto import SessionStarterOptions
from baseline.session.session import Session
from baseline.essay import EssayFactory, FileFactory
from baseline.calculation.criteria.criteria_calculator import CriteriaCalculator
from baseline.calculation.psr.psr_calculator import PsrCalculator
from baseline.satellite.assistant import Assistant
from baseline.satellite.archiver import get_essays_list
from baseline.satellite.archiver import unzip


def min_validate(min_value):
    def inner_min_validate(ctx, param, value):
        if value < min_value:
            raise click.BadParameter(f'{param} минимальное значение {min_value}')
        return value

    return inner_min_validate


@click.group(help="Baseline cli")
def cli():
    """
    Baseline cli
    """


@cli.group(help="Manages session")
def session():
    """Manages session """


@session.command('start', help="Use for start a session with params")
@click.option(
    '--type', '-t', 'session_type',
    type=click.Choice(list(SessionTypeType.__args__)),
    default='algorithmic',
    # prompt=True,
    show_default=True,
    help="Тип сессии, по умолчанию запускается алгоритмическая")
@click.option(
    '--dataset', '-ds', 'dataset',
    type=click.Choice(list(SessionDatasetType.__args__)),
    default='train',
    show_default=True,
    help="Датасет, файлы из которого будут использованы для сессии (применим только в алгоритмической сессии)")
@click.option(
    '--language', '-lang', 'language',
    type=click.Choice(list(SessionLanguageType.__args__)),
    default='rus',
    show_default=True,
    help="""
    Определяет, какие предметы будут будут в сессии
    В "rus" входит - Русский язык, Литература, История, Обществознание
    В "eng" входит - Английский язык
    (применим только в алгоритмической сессии)
    """)
@click.option(
    '--file-count', '-fc',
    type=int,
    default=300,
    show_default=True,
    callback=min_validate(10),
    help="Определяет, сколько файлов будет в сессии (применим только в алгоритмической сессии)")
@click.option(
    '--file-timeout', '-ft',
    type=int,
    default=60,
    callback=min_validate(10),
    show_default=True,
    help="Определяет, какой будет таймаут между доступностью файлов (применим только в алгоритмической сессии)")
def session_start(
        session_type: SessionTypeType,
        dataset: SessionDatasetType,
        language: SessionLanguageType,
        file_count: int,
        file_timeout: int):
    opts = SessionStarterOptions(
        type=session_type,
        dataset=dataset,
        language=language,
        file_count=file_count,
        file_timeout=file_timeout
    )
    logger.info('Session start command')
    asyncio_run(Session().start(opts))


@session.command('abort', help="Use for abort the active session")
def session_abort():
    logger.info('Session abort command')
    asyncio_run(Session().abort())


@session.command('reconnect', help="Use for reconnect to the active session")
def session_reconnect():
    logger.info('Session reconnect command')
    asyncio_run(Session().reconnect())


@cli.group('calc', help="Calculation psr or criteria")
def calc():
    pass


@calc.command('psr', help="Calculate psr")
@click.option(
    '--first-file', '-ff',
    type=str,
    nargs=1,
    required=True,
    # @todo корректно написать о разнице сравнения когда на первом месте алг и эксп разметка
    help="""
    Имя оцениваемого файла в директории (по умолчанию custom, изменить можно параметром --dir)
    """
)
@click.option(
    '--second-file', '-sf', 'second_files',
    type=str,
    multiple=True,
    required=True,
    help="""
    Имена файлов, с которыми будет сравниваться "--first-file" файл, минимум необходимо указать 1 файл
    Чтобы указать больше одного файла нужно для каждого файла использовать свой параметр
    """
)
@click.option(
    '--dir', '-d',
    default='custom',
    show_default=True,
    help="""
    Директория, из которой 
    Должна существовать в директории 'files', поиск начинается с неё
    """
)
@click.option(
    '--mode', '-m',
    type=click.Choice(['normal', 'nomination']),
    default='normal',
    show_default=True,
    help="Режим, в котором запущен ПСР"
)
def calc_psr(first_file: str, second_files: Tuple[str], dir: str, mode: bool):
    first_file_path = 'files/custom/' + first_file
    second_files_ways = ['files/custom/' + item for item in second_files]
    if dir:
        first_file_path = 'files/' + dir + '/' + first_file
        second_files_ways = ['files/' + dir + '/' + item for item in second_files]

    try:
        with open(first_file_path) as f:
            f.readlines()
    except FileNotFoundError as err:
        click.secho('ERROR', bold=True)
        return click.secho(
            'Файл, введенный в параметре first_file ' + first_file_path + ' не найден. Проверьте структуру папок внутри каталога files.',
            bg='red', fg='white')

    try:
        for file_way in second_files_ways:
            with open(file_way) as f:
                f.readlines()
    except FileNotFoundError as err:
        click.secho('ERROR', bold=True)
        return click.secho(
            'Файл из параметра second_files ' + file_way + ' не найден. Проверьте структуру папок внутри каталога files.',
            bg='red', fg='white')

    psr_calculator = PsrCalculator()
    psr_calculator.enter_operand_by_path(first_file_path)
    for file_way in second_files_ways:
        psr_calculator.enter_operand_by_path(file_way)

    psr_calculator.calculate()
    psr_calculator.print_result_to_stdout()


@calc.command('criteria', help="Calculate criteria")
@click.option(
    '--file-name', '-fn',
    type=str,
    required=True,
    help="Имя оцениваемого файла в директории (по умолчанию custom, изменить можно параметром --dir)"
)
@click.option(
    '--dir', '-d',
    default='custom',
    show_default=True,
    help="""
    Директория, в которой будет взят файл эссе
    Должна существовать в директории 'files', поиск начинается с неё
    """
)
@click.option(
    '--save', '-s',
    is_flag=True,
    default=False,
    show_default=True,
    help=""" 
    Флаг говорит о том, что результат будет сохранен в переданный для расчёта файл (файл будет перезаписан).
    """
)
@click.option(
    '--copy', '-c',
    is_flag=True,
    default=False,
    show_default=True,
    help="""
    Флаг позволяет скопировать содержимое эссе + расчитанные критерии в файл, с названием ***_criteria_result.json
    """
)
def calc_criteria(file_name: str, dir: str = '', save: bool = False, copy: bool = False):
    prepared_path = 'files/custom/' + file_name
    if dir:
        prepared_path = 'files/' + dir + '/' + file_name

    try:
        with open(prepared_path) as f:
            f.readlines()
    except FileNotFoundError as err:
        click.secho('ERROR', bold=True)
        return click.secho('Файл ' + file_name + ' не найден. Проверьте структуру папок внутри каталога files.',
                           bg='red', fg='white')

    calculator = CriteriaCalculator()
    calculator.enter_operand_by_path(prepared_path)
    calculator.calculate()
    calculator.print_to_stdout()

    if save:
        calculator.save_result_in_current_file()
    if copy:
        calculator.save_result_in_copy_file()


@cli.group('satellite', help="Satellites command group")
def satellite():
    pass


@satellite.command('work-example', help="")
@click.option(
    '--mode', '-m',
    type=click.Choice(['profacti', 'proocenki', 'proznaniya']),
    required=True,
    help="Вид саттелита"
)
@click.option(
    '--stage', '-s',
    type=click.Choice(['test', 'train', 'final']),
    required=True,
    help="Этап соревнования"
)
def sat(mode, stage):
    try:
        unzip(mode, stage)
        ar_essay = get_essays_list(mode)

        for essay in ar_essay:
            assistanit = Assistant()
            assistanit.get_essay(essay, mode, stage)
            assistanit.get_blank_for_essay()

            answer = random.randint(0, 5)

            assistanit.set_answer(answer)
            assistanit.save_answer_for_essay()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    cli()

# session
#       start --type --dataset --lang --files_timeout --files_count
#       abort --continue
#       reconnect --continue
#       ##future## - на сервере ещё не реализовано
#       get_file - получение текущего файла в сессии)

# calculation
#   psr
#       --files_id <files_id> [0001 0002] (перечень id файла в папке files/custom)
#       --files_path <files_path> [/dir/file.json /dir/file2.json] (перечень путей к файлу относительно папки files | --filePath myDir/filepathWithExtension.json)
#       --dir <dir> files/custom/ (параметр директории, из которой необходимо считывать файлы)
#       --mode <mode> (режим, в котором запущен ПСР - normal/nomination. по-умолчанию - normal)
# @todo take FileCollection
# calculation
#   criteria
#       --fileId <fileId> (id файла в папке files/custom) (/^\d+$/);
#       --filePath <filePath> ('путь к файлу относительно папки files)
#       --dir <dir> (параметр директории, из которой необходимо считывать файлы) ('files/custom/')
#       --save <save> (параметр, позволяющий сохранить результаты расчёта критериев в отдельный файл) (false)
