from typing import Any, Literal


def cast(value, typeof: Literal['bool', 'str', 'int', 'float', 'list', 'dict']) -> Any:
    try:
        match typeof:
            case 'bool':

                if value in (False, None, 'False', 'false', 'No', 'no'):
                    result = False

                else:
                    result = True

            case 'str':
                result = str(value)

            case 'int':
                result = int(value)

            case 'float':
                result = float(value)

            case 'list':
                result = list(value)

            case 'dict':
                result = dict(value)

            case _:
                result = value

        return result

    except TypeError:
        return value


def is_number(value: str):
    try:
        int(value)
        return True

    except ValueError:
        return False


if __name__ == '__main__':
    assert cast(1, 'str') == '1'
    assert cast(1.3, 'int') == 1
    assert cast('1', 'int') == 1
    assert cast(1, 'float') == 1.0
    assert cast('False', 'bool') is False
    assert cast('No', 'bool') is False
    assert cast('No', 'bool') is False
    assert cast('Yes', 'bool') is True
