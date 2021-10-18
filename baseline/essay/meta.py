from abc import ABC
import logging


class MetaValidator:
    @staticmethod
    def validate_fields(fields: dict):

        logging.info('')
        # logging.info(fields)
        # meta_object_dict_rules: dict = {
        #     'id': str,
        #     'subject': str,
        #     'uuid': str,
        #     'class': str,
        #     'theme': str,
        #     'test': str,
        #     'taskText': str,
        #     'expert': str,
        #     'name': str,
        # }
        # for rule in meta_object_dict_rules:
        #     if type(fields[rule]) != meta_object_dict_rules[rule]:
        #         raise TypeError('Поле ' + rule + ' имеет неверный тип.')


class MetaAbstract(ABC):
    _id: str
    _subject: str
    uuid: str = ''
    theme: str = ''
    grade: str = ''  # naming property as 'grade' because 'class' is key word
    year: int = ''
    test: str = ''
    taskText: str = ''
    expert: str = ''
    name: str = ''

    def __init__(self, meta_object: dict = None):
        if meta_object is not None:
            self.fill(meta_object)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: str):
        if value is None or type(value) != str or len(value) == 0:
            raise ValueError('Field "id" in meta required')

        self._id = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value: str):
        if value is None or type(value) != str or len(value) == 0:
            raise ValueError('Field "subject" in meta required')

        self._subject = value

    def to_dict(self):
        return {
            "class": self.grade,
            "id": self.id,
            "name": self.theme,
            "subject": self.subject,
            "taskText": self.taskText,
            "test": self.test,
            "theme": self.theme,
            "uuid": self.uuid,
            "year": self.year
        }

    def fill(self, meta_object: dict) -> None:
        MetaValidator.validate_fields(meta_object)

        self.id = meta_object.get('id')
        self.uuid = meta_object.get('uuid')
        self.theme = meta_object.get('theme') or ''
        self.grade = meta_object.get('class') or ''
        self.year = meta_object.get('year') or ''
        self.test = meta_object.get('test') or ''
        self.subject = meta_object.get('subject')
        self.taskText = meta_object.get('taskText') or ''
        self.expert = meta_object.get('expert') or ''
        self.name = meta_object.get('name') or ''


class Meta(MetaAbstract):
    pass


class MetaFactory:
    @staticmethod
    def get_instance() -> MetaAbstract:
        return Meta()


if __name__ == '__main__':
    meta = MetaFactory.get_instance()
