from .attackable import Attackable


class Base(Attackable):

    def __init__(self, player: str):
        Attackable.__init__(self, 100)
        self.player = player
        self.health = 100  # placeholder
