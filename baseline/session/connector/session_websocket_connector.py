from __future__ import annotations
from pathlib import Path
from typing import NoReturn, Optional, Callable
import json
from loguru import logger

from baseline.essay.file import FileFactory
from baseline.essay.essay import EssayAbstract, EssayFactory
from baseline.tools.constants import SESSION_IS_ONLY_SAVE_FILES
import baseline.session.session as m_session
from baseline.session.connection.connection import ConnectionAbstract
from baseline.session.connection.websocket import Websocket
from baseline.session.connector import exceptions
from baseline.session.connector.session_connector_abstract import SessionConnectorAbstract
from baseline.session.dto import input as dto_input
from baseline.session import exception

from baseline.markup import Marker


class SessionWebsocketConnector(SessionConnectorAbstract):
    _platform_connection: ConnectionAbstract
    _session: m_session.Session

    __callback_after_connect: Optional[Callable] = None

    # can reinit in start and reconnect event
    _logger = logger

    def __init__(self, session: m_session.Session):
        super().__init__(session)

        self._platform_connection = Websocket()

        self._subscribe()

    async def start(self) -> NoReturn:
        if self._session and self._session.id:
            self._logger.error('Previous session is still active. Try to use "reconnect" command')
            raise exceptions.StartSessionError(
                f'Session is exists, id={self._session.id}. Try to use reconnect command')

        async def emit_start():
            # @todo need detect if use start 2 times, because connect can reconnect active session
            self._logger.debug('Emitting session-start after namespace connection')
            await self._platform_connection.emit(
                'session-start',
                options.prepare_to_command()
            )

        self.__callback_after_connect = emit_start

        await self._platform_connection.connect()
        self._logger.info('Start command init')
        options = self._session.options
        self._logger.debug('Start session options', data=options)
        if self._platform_connection.is_connected() and options:
            self._logger.debug('Baseline was connected and run loop')
            await self._platform_connection.wait()
        else:
            self._logger.error(
                'Baseline was not connected or start options are empty', data={
                    'connect': self._platform_connection.is_connected(),
                    'options': options
                }
            )
            raise exceptions.StartSessionError('Baseline was not connected or start options are empty')

    async def abort(self):
        async def emit_abort():
            await self._platform_connection.emit('session-client-abort')

        self.__callback_after_connect = emit_abort

        await self._platform_connection.connect()
        self._logger.info('Abort command init')
        await self._platform_connection.wait()

    async def reconnect(self):
        await self._platform_connection.connect()
        self._logger.info('Reconnect command init')

        async def emit_reconnect():
            await self._platform_connection.emit('session-reconnect')

        self.__callback_after_connect = emit_reconnect

        await self._platform_connection.wait()

    async def send_file(self, essay: EssayAbstract) -> None:
        essay_dict = essay.to_dict()
        self._logger.debug('Emit session-file-send', data=essay_dict)
        if self._platform_connection.is_connected():
            self._logger.info(f'Sending essay id={essay.meta.id} during session id={self._session.id}')
            await self._platform_connection.emit(
                'session-file-send',
                {
                    'sessionId': self._session.id,
                    'fileId': essay.meta.id,
                    # @todo ?????????????? ???????????????? ??????????????, ?? ???? json-????????????
                    'content': json.dumps(essay_dict)
                }
            )
        else:
            self._logger.error('An error occured during sending of essay due to connection lost.')
            raise exceptions.NotConnectedError('WS is not connected')

    async def get_file(self) -> None:
        # not implement on platform
        # here emit event for get active file in session
        pass

    def _subscribe(self):
        self._logger.debug('Subscribing on events')
        self.__subscribe_handlers_default()
        self.__subscribe_handlers_session()
        self.__subscribe_handlers_file()

    def __subscribe_handlers_default(self):
        self._platform_connection.on('connect', self.__handler_connect)
        self._platform_connection.on('disconnect', self.__handler_disconnect)

    def __subscribe_handlers_session(self):
        self._platform_connection.on('connection-auth-error', self.__handler_connection_auth_error)

        self._platform_connection.on('session-start-success', self.__handler_session_start_success)
        self._platform_connection.on('session-start-error', self.__handler_session_start_error)

        self._platform_connection.on('session-reconnect-success', self.__handler_session_reconnect_success)
        self._platform_connection.on('session-reconnect-error', self.__handler_session_reconnect_error)
        self._platform_connection.on('session-auto-reconnect-error', self.__handler_session_auto_reconnect_error)

        self._platform_connection.on('session-close', self.__handler_session_close)

        self._platform_connection.on('session-client-abort-success', self.__handler_session_abort_success)
        self._platform_connection.on('session-client-abort-error', self.__handler_session_abort_error)

    def __subscribe_handlers_file(self):
        self._platform_connection.on('session-file-available', self.__handler_file_available)
        self._platform_connection.on('session-file-send-success', self.__handler_file_send_success)
        self._platform_connection.on('session-file-send-error', self.__handler_file_send_error)

    """
        Handlers for a websocket event
    """

    async def __handler_connect(self):
        self._logger.info(f'Connected on [/pku] namespace.')
        await self.__call_after_connect()

    async def __call_after_connect(self):
        """
        ??????! ?????? ???????????? (4.6) ???????????? ???????????? python-socketio
        ???????????????? ?????????????????????? ?? ??????, ?????? ?????? ???????????????? ?????????????????????? ?? ???????????????????? /pku
        ?? ???????????????????? ???????? emit ?? ?????????????????? ???? ????????????????, ??.??. ?????????????????????? ???????????? ????????????????
        ???????????? ???????????????????? ?????????? ?????????????? ?? ????????????????????, ?????????? ???? ???????????????? ?????? ?????????????????????? ?? ??????????????????
        ?? v5.0.4 ???????????????? ???????????? ?? ????????????

        @todo ???????????????? ?????????? python-socketio ???? ?????????????????? ???????????? ?????????? ???????????? ?????????????????? 3???? ?????????????????? socketio ?? ??????????????????
        @link: https://github.com/nestjs/nest/issues/5676
        @todo ???????????????? ?????????? ???????????????????? ???????????? ?? ?????????? self._client.connect ???????????????? wait=True
        @https://python-socketio.readthedocs.io/en/latest/api.html#socketio.Client.connect

        :return: None
        """
        if self.__callback_after_connect is not None:
            self._logger.debug(f'There is callback with emit, name={self.__callback_after_connect.__name__}')
            try:
                self._logger.info(f'Call {self.__callback_after_connect.__name__}')
                await self.__callback_after_connect()
            except Exception:
                # @todo catch correct errors
                self._logger.exception('Error after connect callback')
            finally:
                self.__callback_after_connect = None

    async def __handler_disconnect(self):
        self._logger.info(f'Disconnected on [/pku] namespace.')

    async def __handler_connection_auth_error(self, data: dict):
        self._logger.debug('__handler_connection_auth_error', data=data)
        message_dto = dto_input.MessageDto(**data)
        self._logger.info(f'Handle auth error. Message: {message_dto.message}')
        self._logger.error('Authotization failed. Please check your token. Disconnect!')
        await self._platform_connection.disconnect()

    def __handler_session_start_success(self, data: dict) -> NoReturn:
        self._logger.debug('__handler_session_start_success', data=data)
        session = dto_input.SessionStartSuccessDto(session_id=data.get('sessionId'))

        if self._session is None:
            self._logger.error('Session does not exist. Correction of init session entity needed.')
            raise exception.SessionNotExistError('Event: session-start-success. Session is None')

        self._logger.success(f'Session id={session.session_id} was started successfuly.')
        self._session.id = session.session_id
        # add context on log message
        self._logger = self._logger.bind(session=self._session.id)

    async def __handler_session_start_error(self, data: dict) -> NoReturn:
        self._logger.debug('__handler_session_start_error', data=data)
        message_dto = dto_input.MessageDto(**data)

        self._logger.error(f'Session was not started. Message: {message_dto.message}')
        self._logger.info(f'Session was not started, check init params. Disconnect!')
        await self._platform_connection.disconnect()

    def __handler_session_reconnect_success(self, data: dict):
        self._logger.debug('__handler_session_reconnect_success', data=data)
        session = dto_input.SessionStartSuccessDto(session_id=data.get('sessionId'))

        self._logger.success(f'Reconnect to session id={session.session_id}')
        if self._session.id is None:
            self._session.id = session.session_id
        # add context on log message
        self._logger = self._logger.bind(session=self._session.id)
        # todo add confirm connection

    async def __handler_session_reconnect_error(self, data: dict):
        self._logger.debug('__handler_session_reconnect_error', data=data)
        message_dto = dto_input.MessageDto(**data)
        self._logger.error('Attempt to reconnect to the active session was failed. '
                           + f'Reason: {message_dto.message}. '
                           + 'Disconnect.')
        await self._platform_connection.disconnect()

    async def __handler_session_auto_reconnect_error(self, data: dict):
        """
        When try reconnect in connect event
        :param data: data sent by the platform
        """
        self._logger.debug('__handler_session_auto_reconnect_error', data=data)
        message_dto = dto_input.MessageDto(**data)
        self._logger.info('Attempt to auto reconnect to the active session was failed. '
                          + f'Reason: {message_dto.message}. '
                          + 'Wait reconnect or stop the application (press Ctrl+C to interrupt.)')

    async def __handler_session_abort_success(self, data: dict):
        self._logger.debug('__handler_session_abort_success', data=data)
        message_dto = dto_input.MessageDto(**data)

        self._logger.success(f'Session {self._session.id} aborted. Message: {message_dto.message}.')
        self._logger.info('Reset connect params and disconnect')
        self._session.reset()
        await self._platform_connection.disconnect()

    async def __handler_session_abort_error(self, data: dict):
        self._logger.debug('__handler_session_abort_error', data=data)
        message_dto = dto_input.MessageDto(**data)
        self._logger.error(f'An error was occurred during the session abort. Message: {message_dto.message}.')
        self._logger.info(f'Abort command returned an error, try again. Disconnect.')
        await self._platform_connection.disconnect()

    async def __handler_session_close(self, data: dict):
        self._logger.debug('__handler_session_close', data=data)
        self._logger.success(f'Session id={self._session.id} is finished!')
        self._session.reset()
        await self._platform_connection.disconnect()

    async def __handler_file_available(self, data: dict) -> NoReturn:
        """
        When the platform send available essay in current session
        :param data: data with essay id and content
        """
        self._logger.debug('__handler_file_available', data=data)

        if not (data.get('fileId') and data.get('content')):
            raise ValueError('In available essay absent "fileId" or "content" fields')

        session_file = dto_input.SessionFileDto(
            session_id=data.get('sessionId'),
            file_id=data.get('fileId'),
            content=data.get('content')
        )
        self._logger.info(
            f'Essay id={session_file.file_id} is available during session id={self._session.id}'
        )

        essay = await self.__create_essay(session_file)

        if not SESSION_IS_ONLY_SAVE_FILES:
            marked_essay = await self.__markup_essay(essay)

            await self.send_file(marked_essay)

    async def __handler_file_send_success(self, data: dict) -> NoReturn:
        self._logger.debug('__handler_file_send_success', data=data)
        send_result_dto = dto_input.SessionFileSendDto(
            session_id=data.get('sessionId'),
            file_id=data.get('fileId'),
            message=data.get('message') or ''
        )

        self._logger.success(
            f'Essay id={send_result_dto.file_id} was accepted by Platform during session id={send_result_dto.session_id}.'
        )

    async def __handler_file_send_error(self, data: dict) -> NoReturn:
        self._logger.debug('__handler_file_send_error', data=data)

        send_result_dto = dto_input.SessionFileSendDto(
            session_id=data.get('sessionId'),
            file_id=data.get('fileId'),
            message=data.get('message') or ''
        )
        self._logger.info(
            f'Essay id={send_result_dto.file_id} was not accepted or accepted with an error by Platform during session id={self._session.id}. Message: {send_result_dto.message}'
        )

    async def __create_essay(self, session_file: dto_input.SessionFileDto):
        self._logger.debug(f'Creation of essay id={session_file.file_id}')
        essay = EssayFactory.get_instance_from_dict(session_file.content)
        await self.__save_essay(essay, 'input')
        self._logger.debug(
            f'Essay id={session_file.file_id} was created and saved to input dir during session id={self._session.id}',
            session_id=self._session.id,
            file_id=essay.meta.id)
        return essay

    async def __markup_essay(self, essay: EssayAbstract) -> EssayAbstract:
        self._logger.debug(
            f'Essay id={essay.meta.id} was marked up during session id={self._session.id}',
        )
        try:
            marker = Marker()
            marked_essay = await marker.markup_async(essay)
        except Exception as error:
            # @todo ???????????????????????????????? ????????????
            self._logger.exception(f'Essay id={essay.meta.id} was not marked up. Error: {error}')
        else:
            await self.__save_essay(marked_essay, 'output')
            self._logger.debug(
                f'Marked up essay id={marked_essay.meta.id} was created and saved to output dir during session id={self._session.id}',
            )
            return marked_essay

    async def __save_essay(self, essay: EssayAbstract, dir_name: str):
        file = FileFactory.create(Path(f'sessions/{self._session.id}/{dir_name}/{essay.meta.id}.json'))
        essay.file = file
        essay.save()
