from enum import Enum

class EntityType(Enum):
    BASE = "BASE"
    ANT = "ANT"
    FOOD = "FOOD"

class Entity:

    def __init__(self, entityId: str, owningPlayer: str, entityType: EntityType):
        self.owningPlayer = owningPlayer
        self.entityId: str = entityId
        self.entityType: EntityType = entityType

    def getId(self) -> str:
        return self.entityId

    def getEntityType(self) -> EntityType:
        return self.entityType

    def getOwner(self) -> str:
        return self.owningPlayer




