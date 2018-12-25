from os import getenv
from enum import Enum, auto
from typing import Union, List, Callable, Dict


ENV_RETURN_TYPE = Union[str, int, Union[List[str], List[int]]]


class SupportedListTypes(Enum):
    STR = auto()
    INT = auto()


class SupportedBaseTypes(Enum):
    STR = auto()
    INT = auto()
    LIST_STR = auto()
    LIST_INT = auto()


def _int_converter(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise InvalidEnvironmentVariableTypeException('Could not convert {} into an int type.'.format(value))


def _list_converter(value: str, list_type: SupportedListTypes) -> Union[List[str], List[int]]:
    if list_type == 'str':
        return value.split(',')
    elif list_type == 'int':
        return [_int_converter(x) for x in value.split(',')]


def process_environment_variable(env: str,
                                 env_optional: bool = False,
                                 env_type: SupportedBaseTypes = SupportedBaseTypes.STR) -> ENV_RETURN_TYPE:
    env_value = getenv(env)

    if not env_value and not env_optional:
        raise MissingEnvironmentVariableException()

    return __ENV_TYPE_CONVERTER[env_type](env_value)


class MissingEnvironmentVariableException(Exception):
    """Raised when an expected environment variable isn't provided"""


class InvalidEnvironmentVariableTypeException(Exception):
    """Raised when a failure occurs when attempting to setup an environment variable's type value"""


__ENV_TYPE_CONVERTER: Dict[SupportedBaseTypes, Callable[[str], ENV_RETURN_TYPE]] = {
    SupportedBaseTypes.STR: lambda x: x,
    SupportedBaseTypes.INT: _int_converter,
    SupportedBaseTypes.LIST_STR: lambda x: _list_converter(x, SupportedListTypes.STR),
    SupportedBaseTypes.LIST_INT: lambda x: _list_converter(x, SupportedListTypes.INT)
}
