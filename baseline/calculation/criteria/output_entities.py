class Criteria: 
    K1: int = 0
    K2: int = 0
    K3: int = 0
    K4: int = 0
    K5: int = 0
    K6: int = 0
    K7: int = 0
    K8: int = 0
    K9: int = 0
    K10: int = 0
    K11: int = 0
    K12: int = 0

    def __init__(self, calc_result: dict):
        self.fill_from_dict(calc_result)

    def fill_from_dict(self, calc_result: dict):
        print(calc_result.get('K1'))
        self.K1 = calc_result.get('K1') or 0
        self.K2 = calc_result.get('K2') or 0
        self.K3 = calc_result.get('K3') or 0
        self.K4 = calc_result.get('K4') or 0
        self.K5 = calc_result.get('K5') or 0
        self.K6 = calc_result.get('K6') or 0
        self.K7 = calc_result.get('K7') or 0
        self.K8 = calc_result.get('K8') or 0
        self.K9 = calc_result.get('K9') or 0
        self.K10 = calc_result.get('K10') or 0
        self.K11 = calc_result.get('K11') or 0
        self.K12 = calc_result.get('K12') or 0

    def to_dict(self):
        prepared_dict = dict((k, v) for k, v in self.__dict__.items() if v is not None)

        return prepared_dict