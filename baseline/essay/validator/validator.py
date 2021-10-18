from typing import List, Any
from jsonschema import Draft4Validator
from baseline.essay.validator.schema import SCHEMA_ESSAY


class EssayValidator:
    _essay: dict
    _errors: List[Any]
    _validator: Draft4Validator

    @staticmethod
    def validate_essay(essay: dict) -> List[Exception]:
        return Draft4Validator(SCHEMA_ESSAY).validate(essay)

    # todo set type EssayAbstract
    def __init__(self, essay: Any):
        self._errors = []
        self._essay = essay.to_dict()
        self._validator = Draft4Validator(SCHEMA_ESSAY)

    def _validate(self, instance: dict):
        validator_iter = self._validator.iter_errors(instance)
        for error in validator_iter:
            self._errors.append(error)

    def is_valid(self) -> bool:
        self._validate(self._essay)
        return len(self._errors) == 0

    def get_errors(self) -> List[str]:
        return list(map(lambda error: f"{'->'.join(list(error.path))}: {error.message}", self._errors))


if __name__ == '__main__':
    validator = Draft4Validator.check_schema(SCHEMA_ESSAY)
