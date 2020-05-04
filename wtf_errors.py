"""All errors used in the WTF interperter"""

class WtfError():
    """A base class for all Errors"""

class UnknownCharacterError(WtfError):
    """An error which declares that an unknown character was used as a command in the source file"""
    def __init__(self, character: str, line: str, line_nr: int, character_nr: int):
        self.character = character
        self.line = line
        self.character_nr = character_nr
        self.line_nr = line_nr

    def __str__(self):
        return "ERROR: Unknown character (combination) in line " + str(self.line_nr) + \
            " at word number " + str(self.character_nr) + \
            ": '" + str(self.character) + "' in word " + str(self.line)

    def __repr__(self):
        return self.__str__()
