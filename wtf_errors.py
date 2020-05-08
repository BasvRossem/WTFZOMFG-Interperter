"""All errors used in the WTF interperter"""
from typing import TypeVar

from wtf_objects import Token


class WtfError():
    """A base class for all Errors"""

    def __str__(self) -> str:
        return str(type(self).__name__)

    def __repr__(self) -> str:
        return self.__str__()


class UnknownCharacterError(WtfError):
    """An error which declares that an unknown character was used as a command in the source file"""

    def __init__(self, character: str, line: str, line_nr: int, character_nr: int) -> None:
        self.__character = character
        self.__line = line
        self.__character_nr = character_nr
        self.__line_nr = line_nr

    def __str__(self) -> str:
        return str(type(self).__name__) + ": Unknown character (combination) in line " + \
            str(self.__line_nr) + " at word number " + str(self.__character_nr) + ": '" + \
            str(self.__character) + "' in word '" + str(self.__line) + "'"

    def __repr__(self) -> str:
        return self.__str__()


class UnknownTokenError(WtfError):
    """An error which declares that a token does not have an associated function"""

    def __init__(self, token: Token) -> None:
        self.__token = token

    def __str__(self) -> str:
        return str(type(self).__name__) + \
            ": Unknown token " + str(self.__token) + \
            ", token has no associated function"

    def __repr__(self) -> str:
        return self.__str__()


class UnknownTypeError(WtfError):
    """An error which declares that a different type expected"""
    A = TypeVar('A')
    B = TypeVar('B')

    def __init__(self, expected: A, given: B) -> None:
        self.__expected = expected
        self.__given = given

    def __str__(self) -> str:
        return str(type(self).__name__) + \
            ": Wrong type, expected '" + str(type(self.__expected).__name__) + \
            "' got '" + str(type(self.__given).__name__) + "'"

    def __repr__(self) -> str:
        return self.__str__()


class NotNumericError(WtfError):
    """An error which declares that a number was expected"""
    A = TypeVar('A')
    def __init__(self, given: A) -> None:
        self.__given = given

    def __str__(self) -> str:
        return str(type(self).__name__) + \
            ": Wrong type, expected a numeric value, got '" + \
            str(self.__given) + "'"

    def __repr__(self) -> str:
        return self.__str__()


class OutOfBoundsError(WtfError):
    """An error which declares that a number was expected"""

    def __init__(self, memory_size: int, position: int) -> None:
        self.__memory_size = memory_size
        self.__position = position

    def __str__(self) -> str:
        return str(type(self).__name__) + \
            ": Cannot reach position '" + str(self.__position) + \
            "', memory is " + str(self.__memory_size) + " cells large"

    def __repr__(self) -> str:
        return self.__str__()


class WrongDivisionError(WtfError):
    """An error which declares that a the denominator was zero"""

    def __init__(self, value: int) -> None:
        self.__value = value

    def __str__(self) -> str:
        return str(type(self).__name__) + ": Cannot divide by '" + str(self.__value) + "'"

    def __repr__(self) -> str:
        return self.__str__()
