from datetime import datetime
from typing import Any, Dict, List, Literal


def cast(value: Any, typeof: Literal['bool', 'str', 'int', 'float', 'list', 'dict', 'datetime.fromtimestamp', 'datetime.fromisoformat'] or str) -> (bool, str, int, float, list, dict, datetime):
    """
    Converts a value into a specific type based on a parameter which is a string representation of the desired type.

    Parameters:
    value (Any): The value to be converted.
    typeof (Literal['bool', 'str', 'int', 'float', 'list', 'dict', 'datetime.fromtimestamp', 'datetime.fromisoformat']): The string representation of the target type.

    Returns:
    Union[bool, str, int, float, list, dict, datetime]: The converted value or None if the conversion fails or if the target type is not supported.
    """

    type_mapping = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'list': list,
        'dict': dict,
        'datetime.fromtimestamp': datetime.fromtimestamp,
        'datetime.fromisoformat': datetime.fromisoformat
    }

    if typeof in type_mapping:
        try:
            if typeof == 'bool':
                if value in (False, None, 'False', 'false', 'No', 'no'):
                    result = False
                else:
                    result = True
            else:
                result = type_mapping[typeof](value)

            return result

        except ValueError:
            return None

    else:
        return None


def delimiter_list_to_string(value: list, delimiter: str) -> str:
    """
    Splits a string into a list based on a delimiter. This is especially useful when changing a rich Table output to
    span multiple lines using '\n'.
    :param value: A list to join
    :param delimiter: The delimiter to use when joining the list
    :return: A delimited string
    """
    return delimiter.join(value)


def is_number(value: str) -> bool:
    """
    Determines if a value is a number.
    :param value: The value to check.
    :return: A boolean indicating if the value is a number.
    """
    try:
        int(value)
        return True

    except ValueError:
        return False


def key_value_list_to_dict(value: List[Dict], key_name: str = 'Key', value_name: str = 'Value') -> dict:
    """
    Converts a list of dictionaries to a dictionary of key value pairs. A common example of this usage is converting
    AWS Tags lists of [{Key: 'Name', Value: 'MyName'}] to {'Name': 'MyName'}.
    :param value: List of dictionaries
    :param key_name: The key name to use for the key in the dictionary
    :param value_name: The key name to use for the value in the dictionary
    :return: A dictionary of key value pairs
    """
    return {item[key_name]: item.get(value_name) for item in value if key_name in item.keys()}


if __name__ == '__main__':
    assert cast(1, 'str') == '1'
    assert cast(1.3, 'int') == 1
    assert cast('1', 'int') == 1
    assert cast(1, 'float') == 1.0
    assert cast('False', 'bool') is False
    assert cast('No', 'bool') is False
    assert cast('No', 'bool') is False
    assert cast('Yes', 'bool') is True
