from datetime import datetime


def convert_env_boolean(env_value: str) -> bool:
    """ Converts an envvar string into a boolean.  Rules: true/True/TRUE/t/T/1 -> True;  All others false

    >>> convert_env_boolean('t')
    True

    >>> convert_env_boolean('1')
    True

    >>> convert_env_boolean('0')
    False
    """
    return env_value.lower() in ['true', '1', 't']


def construct_timestamp(param: str):
    return datetime.strptime(param, "%Y-%m-%d %H:%M:%S")
