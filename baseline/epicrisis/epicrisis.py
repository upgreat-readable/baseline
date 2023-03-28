from abc import ABC
from baseline.epicrisis.copy_abstract import CopyAbstract
from baseline.session.dto import input as dto_input

class EpicrisisAbstract(CopyAbstract, ABC):
    session_id: int
    epicrisis_id: int
    version_id: int
    team_id: int
    task_id: int
    session_type_code: int
    awsLink: str
    path_to_xml: str


    def __init__(self, data: dto_input.SessionFileDto):

        self.path_to_xml = '/sessions/sessionId/epicrisisId_versionId_taskId.xml'

