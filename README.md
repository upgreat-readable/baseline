# Baseline участников конкурса Про//чтение

[Пакет baseline](/docs/baseline.md)
- [модуль работы с эссе](/docs/essay.md) `baseline.file`;
- [модуль сессий обмена с платформой](/docs/session.md) `baseline.session`;
- [модуль разметки эссе](/docs/markup.md) `baseline.markup`;
- [вспомогательные инструменты](/docs/tools.md) `baseline.tools`
- [инструмент для работы с саттелитами](/docs/satellite.md) `baseline.satellite`

[Консольный интерфейс](/docs/cli.md) для управления сессиями обмена и оценивания эссе

Зависимости:
  - pipenv, для виртуализации и управления зависимостями
  - Python 3.9
  - python-socketio["asyncio-client"] версия ~=4.6
    > важно соблюдать версию пакета, т.к. Nestjs gateway поддерживает только 2 версию протакола socketio, ждем 8й версии nestjs чтобы обновить пакет 
  - aiohttp
  - click
  - loguru

Увидеть все зависимости можно в файле `Pipfile`

Развертывание и установка:
1) Удостовериться, что на локальной машине есть python 3.9 версии.
    > для установки использовать `sudo apt install python3.9` или альтернативу в вашем дистрибутиве
2) Установить pipenv утилиту `pip3 install pipenv`
    > После установки утилиты она может быть не доступна в терминале по имени. 
    > Либо используйте полный путь до утилиты, либо добавьте в $PATH
3) Выполнить `pipenv install` в корне проекта для создания виртуального окружения, и установки в нем всех необходимых зависимостей
    > зависимости устанавливаются согласно файлу Pipfile.lock по этому необходимо держать его в актуальном состоянии
4) Активировать виртуальное окружение `pipenv shell`
5) Создать файл .env на основе примера: `cp .example.env .env` и заполнить поле TOKEN (для участников Саттелитов это не нужно) 
6) Установить пакет baseline, для этого выполнить `python setup.py install` в корне проекта   

> Для комфортной работы, с подсказками, необходимо настроить IDE или редактор на то, чтобы искал пакеты именно из виртуального окружения

### TODO
- сгенерировать requirements.txt файла на основе Pipfile.lock, обновлять его во время CI
- обновить пакет python-socketio до 5+ версии, когда платформа будет поддерживать протокол 3-й версии socketio