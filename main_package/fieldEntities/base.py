import main_package.field as field
from main_package.interfaces.attackable import Attackable


class Base(Attackable):

    def __init__(self, player: str):
        Attackable.__init__(self, 100)
        self.fieldPosition: field.Field = None
        self.player = player
        self.health = 100  # placeholder
