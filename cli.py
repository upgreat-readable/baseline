import random
import subprocess

import click
import os.path
from typing import Tuple
from pathlib import Path
from loguru import logger

from baseline.tools.constants import SessionContestType, SessionStageType, SessionDatasetType
from baseline.tools.run import asyncio_run
from baseline.session.dto import SessionStarterOptions
from baseline.session.session import Session
from baseline.essay import EssayFactory, FileFactory
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
    '--contest', '-c', 'contest',
    type=click.Choice(list(SessionContestType.__args__)),
    default='finder',
    # prompt=True,
    show_default=True,
    help="Тип конкурса, по умолчанию запускается finder")
@click.option(
    '--stage', '-stage', 'stage',
    type=click.Choice(list(SessionStageType.__args__)),
    default='qualifying',
    show_default=True,
    help="""
    Этап конкурса, который будет участвовать в обмене
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
        contest: SessionContestType,
        stage: SessionStageType,
        file_count: int,
        file_timeout: int):
    opts = SessionStarterOptions(
        contest=contest,
        stage=stage,
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
