import main_package.field as field
from main_package.interfaces.Entity import Entity, EntityType
from main_package.interfaces.attackable import Attackable


class Base(Entity, Attackable):

    def __init__(self, player: str):
        Entity.__init__(self, self.__hash__().__str__(), player, EntityType.BASE)
        Attackable.__init__(self, 100)
        self.fieldPosition: field.Field = None
        self.player = player
        self.health = 100  # placeholder
