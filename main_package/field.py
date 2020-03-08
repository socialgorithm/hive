from enum import Enum
import logging
from typing import Tuple

import main_package.fieldEntities.ant as ant
import main_package.fieldEntities.food as food
import main_package.fieldEntities.base as base
from colorama import init, Fore

from main_package.interfaces.Entity import Entity, EntityType

init()
logging.basicConfig(level=logging.INFO)


class FieldTypeEnum(Enum):
    EMPTY = Fore.LIGHTBLACK_EX + "E"
    BASE = Fore.RED + "B"
    ANT = Fore.BLUE + "A"
    FOOD = Fore.GREEN + "F"


class Field:
    log = logging.getLogger(__name__)

    def __init__(self, xpos: int, ypos: int):
        self.xpos = xpos
        self.ypos = ypos
        self.type = FieldTypeEnum.EMPTY
        self.entity: Entity = None

    def getPos(self) -> Tuple[int, int]:
        return self.xpos, self.ypos

    def resetToEmpty(self):
        self.type = FieldTypeEnum.EMPTY
        self.entity = None

    def setEntity(self, entity: Entity) -> bool:
        if self.entity is not None:
            self.log.error("Cannot set entity on field that is {} instead of empty".format(self.type))
            return False
        if entity.getEntityType() == EntityType.ANT:
            self.type = FieldTypeEnum.ANT
        elif entity.getEntityType() == EntityType.FOOD:
            self.type = FieldTypeEnum.FOOD
        elif entity.getEntityType() == EntityType.BASE:
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
