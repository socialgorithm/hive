
class Attackable:

    def __init__(self, health):
        self.health = health

    def takeDamage(self, damageAmmount):
        self.health -= damageAmmount

    def isDead(self):
        return self.health <= 0

