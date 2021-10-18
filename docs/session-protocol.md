## Протокол взаимодействия с платформой

Использует websocket протокол для функционала квалификационных и финальных сессий испытаний,
с надстройкой в виде [socketio](https://socket.io/docs/v4) библиотеки.  
На платформе (сервер) используется socketio протокол 2-й версии, это нужно учитывать при реализации клиента.

Для подключения к платформе необходимо указать хост `https://ds.readable.upgreat.one`,
а так же обязательно добавить в строку адреса get-параметр `token` участника (его можно взять в ЛК участника).  
Итоговая строка для подключения должна выглядеть примерно так - `https://ds.readable.upgreat.one/pku?token=<ТОКЕН_УЧАСТНИКА>`.  
Неймспейс для работы с платформой - `/pku`.  
Если токен не указан или он не валидный, то сервер отправит клиенту событие **`connection-auth-error`** и отключит клиента.

### Сигналы для клиента после подключения
> **`connection-auth-error`** - если был передан не валидный токен, соединение закрывается
>>  Payload:
>>  - _`message`_ - (string, required) сообщение или код ошибки

### Старт сессии обмена
##### Сигнал от клиента
> **`session-start`** - начать сессию
>>  Payload:
>>  - _`type`_ - (string, required) тип сессии
      Возможные значения: `algorithmic, technical, final`
>>  - _`params`_ - (object, required) входные параметры
>>>    - _`dsType`_ - (string, optional) тип датасета откуда будут браться файлы (только для алгоритмич. сессии)
         Возможные значения: `train, test`
>>>    - _`countFiles`_ - (number, optional) количество файлов в сессии (только для алгоритмич. сессии)
>>>    - _`lang`_ - (string, optional) язык предметов эссе (только для алгоритмич. сессии)
>>>    - _`time`_ - (number, optional) время таймаута между доступностью файлов (только для алгоритмич. сессии)

##### Ответный сигнал от сервера
> **`session-start-success`** - сессия успешно начата
>>  Payload:
>>  - _`sessionId`_ - (string, required) id сессии

> **`session-start-error`** - создание сессии завершилось ошибкой
>>  Payload:
>>  - _`message`_ - (string, required) сообщение или код ошибки

### Процесс сессии обмена
##### Сигнал от сервера
> **`session-file-avaiable`** - файл доступен
>>  Payload:
>>  - _`sessionId`_ - (string, optional) id сессии
>>  - _`fileId`_ - (string, required) id файла, который стал доступен на платформе, признак того что его можно скачать
>>  - _`content`_ - (string, required) файл в json строке

#### Сигнал от клиента на отправку результата
> **`session-file-send`** - отправить результат разметки файла
>>  Payload:
>>  - _`sessionId`_ - (string, required) id сессии
>>  - _`fileId`_ - (string, required) id файла
>>  - _`content`_ - (string, required) файл в json строке с разметкой

##### Ответный сигнал от сервера
> **`session-file-send-success`** - успешная отправка файла, сохранили на платформе
>>  Payload:
>>  - _`sessionId`_ - (string, required) id сессии
>>  - _`fileId`_ - (string, required) id файла

> **`session-file-send-error`** - ошибочная отправка файла, может произойти сохранение или нет, но не будет засчитан
>>  Payload:
>>  - _`sessionId`_ - (string, required) id сессии
>>  - _`fileId`_ - (string, required) id файла
>>  - _`message`_ - (string, optional) сообщение или код причины

### Окончание сессии обмена
#### Сигнал от сервера, что сессия остановлена
> **`session-close`** - сигнал о том, что сессия доведена до конца
>>  Payload:
>>  - _`sessionId`_ - (string, required) id сессии
>>  - _`type`_ - (string, required) тип завершения, finish или timeout-close

> **`session-abort`** - принудительное окончание сессии, со стороны сервера
>>  Payload:
>>  - _`sessionId`_ - (string, required) id сессии
>>  - _`message`_ - (string, optional) сообщение или код причины

#### Сигнал от клиента на отмену сессии
> **`session-cliend-abort`** - принудительное окончание сессии, со стороны клиента
>>  Payload:
>>  - _`sessionId`_ - (string, required) id сессии
>>  - _`message`_ - (string, optional) сообщение или код причины

##### Ответный сигнал от сервера
> **`session-cliend-abort-success`** - сессия отменена, обмен остановлен
>>  Payload:
>>  - _`message`_ - (string, required) сообщение или код причины

##### Ответный сигнал от сервера
> **`session-cliend-abort-error`** - сессия отменена, обмен остановлен
>>  Payload:
>>  - _`message`_ - (string, required) сообщение или код причины
