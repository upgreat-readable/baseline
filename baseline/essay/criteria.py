from abc import ABC

class CriteriaAbstract(ABC):
    K1: int
    K2: int
    K3: int
    K4: int
    K5: int
    K6: int
    K7: int
    K8: int
    K9: int
    K10: int
    K11: int
    K12: int

    def to_dict(self):
        prepared_dict = dict((k, v) for k, v in self.__dict__.items() if v is not None)

        return prepared_dict

    def fill(self, criteria_object: dict) -> None : 

        self.K1 = criteria_object.get('K1') or 0
        self.K2 = criteria_object.get('K2') or 0
        self.K3 = criteria_object.get('K3') or 0
        self.K4 = criteria_object.get('K4') or 0
        self.K5 = criteria_object.get('K5') or 0
        self.K6 = criteria_object.get('K6') or 0
        self.K7 = criteria_object.get('K7') or 0
        self.K8 = criteria_object.get('K8') or 0
        self.K9 = criteria_object.get('K9') or 0
        self.K10 = criteria_object.get('K10') or 0
        self.K11 = criteria_object.get('K11') or 0
        self.K12 = criteria_object.get('K12') or 0

class Criteria(CriteriaAbstract):
    pass

class CriteriaFactory:
    @staticmethod
    def get_instance() -> CriteriaAbstract:
        return Criteria()


if __name__ == '__main__':
    meta = CriteriaFactory.get_instance()