import operator
from collections import OrderedDict
from re import findall
from typing import List

_MATCH_OPERATIONS = {
        '==': operator.eq,  # Checks if 'a' is equal to 'b'
        '>': operator.gt,   # Checks if 'a' is greater than 'b'
        '<': operator.lt,   # Checks if 'a' is less than 'b'
        '>=': operator.ge,  # Checks if 'a' is greater than or equal to 'b'
        '<=': operator.le,  # Checks if 'a' is less than or equal to 'b'
        '!=': operator.ne,  # Checks if 'a' is not equal to 'b'
        '=': findall        # Checks if 'a' contains 'b'
    }


class HarvestMatch:
    def __init__(self, record: OrderedDict, syntax: str):
        self._record = record
        self._input = syntax
        self.key = None
        self.value = None

        self.operator = [op for op in _MATCH_OPERATIONS.keys() if op in syntax][0]
        self.final_match_operation = None
        self.is_match = None

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
        if self.operator == '=':
            result = findall(_value, _key, IGNORECASE)

        else:
            result = _MATCH_OPERATIONS[self.operator](_key, _value)

        self.final_match_operation = f'{_key} {self.operator} {_value}'

        self.is_match = result

        return result


class HarvestMatchSet(list):
    def __init__(self, record: OrderedDict, syntax: str, matches: List[str]):
        super().__init__()

        self.original_syntax = syntax
        self._record = record

        self.matches = [HarvestMatch(record=record, syntax=match) for match in matches]
