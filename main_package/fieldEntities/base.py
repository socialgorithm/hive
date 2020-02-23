import main_package.field as field


class Base:

    def __init__(self, player: str):
        self.fieldPosition: field.Field = None
        self.player = player
        self.health = 100  # placeholder
