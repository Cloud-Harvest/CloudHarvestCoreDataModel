from typing import List

from collections import OrderedDict


_MATCH_OPERATIONS = (
    '<=',       # less than or equal to
    '>=',       # greater than or equal to
    '==',       # literal equals
    '!=',       # does not equal regex expression
    '<',        # less than
    '>',        # greater than
    '='         # regrex operation
)


class HarvestMatchSet(list):
    def __init__(self, record: OrderedDict, syntax: str, matches: List[str]):
        super().__init__()

        self.original_syntax = syntax
        self._record = record

        self.matches = [HarvestMatch(record=record, syntax=match) for match in matches]


class HarvestMatch:
    def __init__(self, record: OrderedDict, syntax: str):
        self._record = record
        self._input = syntax
        self.key = None
        self.value = None

        self.operator = self._get_operator()
        self.final_match_operation = None
        self.is_match = None

    def _get_operator(self):
        operator = None
        for m in _MATCH_OPERATIONS:
            if m in self._input:
                operator = m
                break

        if operator is None:
            raise Exception(f'No valid match expression operator. Valid match operators are: {_MATCH_OPERATIONS}')

        return operator

    def match(self) -> bool:
        self.key, self.value = self._input.split(self.operator, maxsplit=1)

        # check if there is a function being performed on the self.key or self.value
        from re import match
        if match('^.*\\(.*\\)$', self.key):
            function = self.key[0:str(self.key).find('(')]
            arguments = self.key[str(self.key).find('(') + 1:-1].split(',')
            self.key = arguments[0]
            arguments[0] = self._record.get(self.key)

            from importlib import import_module
            functions = import_module('functions')

            _key = getattr(functions, function)(*arguments)

        else:
            _key = self._record.get(self.key)

        from functions import is_number
        _key_is_number = is_number(value=_key)

        # check if there are any function calls in this part of the match logic
        if match('^.*\\(.*\\)$', self.value):
            function = self.value[0:str(self.value).find('(')]
            arguments = self.value[str(self.value).find('(') + 1:str(self.value).find(')')].split(',')

            from importlib import import_module
            functions = import_module('functions')

            _value = getattr(functions, function)(*arguments)

        else:
            _value = self.value

        # automatically cast the _value as a number if the _key is a number and the _value can be expressed as a number
        _value = float(_value) if isinstance(_key, (int or float)) and is_number(value=_value) else _value

        from re import findall, IGNORECASE
        result = None
        match self.operator:
            case '=':
                if isinstance(_key, str) and isinstance(_value, str):
                    result = len(findall(pattern=str(_value), string=str(_key), flags=IGNORECASE)) > 0

                else:
                    result = _key == _value

            case '<=':
                result = _key <= _value

            case '>=':
                result = _key >= _value

            case '==':
                result = _key == _value

            case '!=':
                if isinstance(_key, str) and isinstance(_value, str):
                    result = len(findall(pattern=str(_value), string=str(_key), flags=IGNORECASE)) == 0

                else:
                    result = _key != _value

            case '<':
                result = _key < _value

            case '>':
                result = _key > _value

        self.final_match_operation = f'{_key} {self.operator} {_value}'

        self.is_match = result

        return result

    def as_mongo_match(self) -> dict:
        key = f'${self.key}'

        match self.operator:
            # https://www.mongodb.com/docs/manual/reference/operator/aggregation/regexMatch/
            case '=':
                result = {
                    "$regexMatch": {
                        "input": key,
                        "regex": self.value
                    }
                }

            case '<=':
                # https://www.mongodb.com/docs/manual/reference/operator/aggregation/lte/
                result = {
                    "$lte": {
                        [
                            key,
                            self.value
                        ]
                    }
                }

            case '>=':
                # https://www.mongodb.com/docs/manual/reference/operator/aggregation/gte/
                result = {
                    "$gte": {
                        [
                            key,
                            self.value
                        ]
                    }
                }
            case '==':
                # https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/
                result = {
                    self.key: self.value
                }
            case '!=':
                # https://www.mongodb.com/docs/manual/reference/operator/aggregation/ne/
                # https://www.mongodb.com/docs/manual/reference/operator/aggregation/regexMatch/
                result = {
                    "$ne": [
                        {
                            "$regexMatch": {
                                "input": key,
                                "pattern": self.value
                            }
                        }
                    ]
                }

            case '<':
                # https://www.mongodb.com/docs/manual/reference/operator/aggregation/lt/
                result = {
                    "$lt": {
                        [
                            key,
                            self.value
                        ]
                    }
                }

            case '>':
                # https://www.mongodb.com/docs/manual/reference/operator/aggregation/gt/
                result = {
                    "$gt": {
                        [
                            key,
                            self.value
                        ]
                    }
                }

            case _:
                raise ValueError('No valid matching statement returned')

        return result


class HarvestRecord(OrderedDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.matching_expressions = []
        self.non_matching_expressions = []

    def key_rename(self, old_key, new_key):
        self[old_key] = new_key

    def match(self, match_statement: str):
        match = HarvestMatch(record=self, syntax=match_statement)
        match.match()

        if match.is_match:
            self.matching_expressions.append(match_statement)

        else:
            self.non_matching_expressions.append(match_statement)

        return match.is_match

    def name_value_to_dict(self, source_column: str, target_column: str, name_key: str = 'Name',
                           value_key: str = 'Value', preserve_original: bool = False):

        self[target_column] = {item[name_key]: item[value_key]
                               for item in self.get(source_column) or []
                               if item.get(name_key)}

        if not preserve_original:
            self.pop(source_column)

        return self


if __name__ == '__main__':
    test_data = {
        "StringTest": "ABCD",
        "IntTest": 7,
        "FloatTest": 5.5,
        "BoolTest": True
    }

    hr = HarvestRecord(**test_data)

    # case-insensitive regex match
    assert hr.match('StringTest=b')

    # literal match
    assert hr.match('StringTest==ABCD')

    # int match
    assert hr.match('IntTest=cast(7,int)')
    assert hr.match('IntTest==cast(7,int)')
    assert hr.match('cast(IntTest,str)==cast(7,str)')
    assert hr.match('IntTest>6')
    assert hr.match('IntTest>=6')
    assert hr.match('IntTest>=7')
    assert hr.match('IntTest<8')
    assert hr.match('IntTest<=8')
    assert hr.match('IntTest<=7')

    # float match
    assert hr.match('FloatTest=5.5')
