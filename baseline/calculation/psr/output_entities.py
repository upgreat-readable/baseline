from collections import namedtuple
from typing import List
import json

class Metrics:
    M1: int = 0
    M2: int = 0
    M3: int = 0
    M4: int = 0
    M5: int = 0
    M6: int = 0
    M7: int = 0

    def fill_from_dict(self, metrics):
        self.M1 = metrics.get('M1') or ''
        self.M2 = metrics.get('M2') or ''
        self.M3 = metrics.get('M3') or ''
        self.M4 = metrics.get('M4') or ''
        self.M5 = metrics.get('M5') or ''
        self.M6 = metrics.get('M6') or ''
        self.M7 = metrics.get('M7') or ''

class PreparedMatchingElement:
    markupId: str = ''
    metrics: dict

    def fill_from_dict(self, match_pair: dict):
        self.id = match_pair['markupId']
        self.metrics = Metrics().fill_from_dict(match_pair['metrics'])


class ComparisonResult:
    id: str
    matching: List[PreparedMatchingElement]

    def fill_from_dict(self, comparison_result: dict):
        self.id = comparison_result['id']
        self.matching = []
        for match_pair in comparison_result['matching']:
            match_temp = PreparedMatchingElement().fill_from_dict(match_pair)
            self.matching.append(match_temp)


class ComparisonResultCollection:
    collection: List[ComparisonResult]

    def native_fill_from_dict(self, psr_result_raw: dict):
        self.collection = []
        for psr_result in psr_result_raw['markups']:
            comparison_temp = ComparisonResult().fill_from_dict(psr_result)
            self.collection.append(psr_result)
            print(psr_result)

    def to_json(self):
      return json.dumps(self.collection, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4, ensure_ascii=False)

## Пример возвращаемого калькулятором формата
"""{'markups':
   [
    {'id': '0001645', 'matching': 
      [
        {'markupId': '20001645',
         'metrics': {'M1': 100.0, 'M2': 100.0, 'M3': 100.0, 'M4': 100.0, 'M5': 100.0, 'M6': 0.0, 'M7': 0, 'MTotal': 83.33}, 'third': False}, 
        {'markupId': '30001645',
         'metrics': {'M1': 100.0, 'M2': 100.0, 'M3': 100.0, 'M4': 100.0, 'M5': 100.0, 'M6': 0.0, 'M7': 0, 'MTotal': 83.33}, 'third': False}
      ], 'STAR': 0, 'STER': 83.33, 'OTAR': 0, 'isExp': True},
    {'id': '20001645', 'matching': 
      [
        {'markupId': '0001645',
         'metrics': {'M1': 100.0, 'M2': 100.0, 'M3': 100.0, 'M4': 100.0, 'M5': 100.0, 'M6': 0.0, 'M7': 0, 'MTotal': 83.33}, 'third': False},
        {'markupId': '30001645',
         'metrics': {'M1': 100.0, 'M2': 100.0, 'M3': 100.0, 'M4': 100.0, 'M5': 100.0, 'M6': 0.0, 'M7': 0, 'MTotal': 83.33}, 'third': False}
      ], 'STAR': 0, 'STER': 83.33, 'OTAR': 0, 'isExp': True}, 
    {'id': '30001645', 'matching': 
      [
        {'markupId': '0001645',
         'metrics': {'M1': 100.0, 'M2': 100.0, 'M3': 100.0, 'M4': 100.0, 'M5': 100.0, 'M6': 0.0, 'M7': 0, 'MTotal': 83.33}, 'third': False},
        {'markupId': '20001645',
         'metrics': {'M1': 100.0, 'M2': 100.0, 'M3': 100.0, 'M4': 100.0, 'M5': 100.0, 'M6': 0.0, 'M7': 0, 'MTotal': 83.33}, 'third': False}
        ], 'STAR': 0, 'STER': 83.33, 'OTAR': 0, 'isExp': True}
    ], 
     'STER_AVG': 83.33,
     'essayId': '0001645'}"""

