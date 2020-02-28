from enum import Enum
import logging
from typing import Tuple

import main_package.fieldEntities.ant as ant
import main_package.fieldEntities.food as food
import main_package.fieldEntities.base as base
from colorama import init, Fore

init()
logging.basicConfig(level=logging.INFO)

class FieldTypeEnum(Enum):
    BASE = Fore.RED + "B"
    ANT = Fore.BLUE + "A"
    FOOD = Fore.GREEN + "F"

    GRASS = Fore.LIGHTBLACK_EX + "g"
    FOREST = Fore.LIGHTBLACK_EX + "F"
    WATER = Fore.LIGHTBLACK_EX + "w"
    DEEP_WATER = Fore.LIGHTBLACK_EX + "W"
    ROCK = Fore.LIGHTBLACK_EX + "R"
    SAND = Fore.LIGHTBLACK_EX + "S"
    DRY_GRASS = Fore.LIGHTBLACK_EX + "D"
    TALL_GRASS = Fore.LIGHTBLACK_EX + "G"
    
class Field:
    log = logging.getLogger(__name__)

    def __init__(self, xpos:int, ypos:int, type: FieldTypeEnum):
        self.xpos = xpos
        self.ypos = ypos
        self.emptyType = type
        self.type = type
        self.entity = None

    def getPos(self) -> Tuple[int, int]:
        return self.xpos, self.ypos

    def resetToEmpty(self):
        self.type = self.emptyType
        self.entity = None

    def setEntity(self, entity) -> bool:
        if self.entity is not None:
            self.log.error("Cannot set entity on field that is {} instead of empty".format(self.type))
            return False
        if isinstance(entity, ant.Ant):
            self.type = FieldTypeEnum.ANT
        elif isinstance(entity, food.Food):
            self.type = FieldTypeEnum.FOOD
        elif isinstance(entity, base.Base):
            self.type = FieldTypeEnum.BASE
        else:
            self.log.error("Entity is of unknown type. Cannot set field type.")
            return False
        self.entity = entity
        entity.fieldPosition = self
        self.log.info("Field ({},{}) set to type {}".format(self.xpos, self.ypos, self.type))
        return True

    def __str__(self):
        return str(self.type.value)