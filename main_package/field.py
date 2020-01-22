from enum import Enum
from colorama import init, Fore, Back, Style
init()

class FieldTypeEnum(Enum):
    EMPTY = Fore.LIGHTBLACK_EX + "E"
    BASE = Fore.RED + "B"
    ANT = Fore.BLUE + "A"
    FOOD = Fore.GREEN + "F"

class Field:

    def __init__(self, xpos:int, ypos:int):
        self.xpos = xpos
        self.ypos = ypos
        self.type = FieldTypeEnum.EMPTY

    def __str__(self):
        return str(self.type.value)