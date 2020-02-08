from main_package.field import Field
from main_package.fieldEntities.food import Food

class Ant:

    def __init__(self, antId: str, currentField: Field):
        self.antId: str = antId
        self.health: int = 100  # how many hitpoints the ant can lose before death
        self._maxFoodCapacity: int = 6  # how much food the ant can carry
        self.currentFood: int = 0 # how much the anti is currently carrying
        self.attackDamage: int = 1  # the damage the ant inflicts per attack
        self._foodUptakeSpeed: int = 2  # how much food the ant acquires per feed action
        self.movementEfficiency: int = 2 # TODO how many fields the ant can move before using 1 food, not yet implemented
        self.fieldPosition: Field = currentField

    def getFoodUptakeValue(self):
        """
        Calculates the maximum amount of food the ant can pick up this action
        :return:
        """
        if self._maxFoodCapacity - self.currentFood >= self._foodUptakeSpeed:
            return self._foodUptakeSpeed
        else:
            return self._maxFoodCapacity - self.currentFood

    def feed(self, food: Food) -> bool:
        obtainedFood = food.getFood(self.getFoodUptakeValue())
        self.currentFood += obtainedFood
        return obtainedFood > 0

    def doAttack(self, otherAnt: 'Ant'):
        otherAnt.health -= self.attackDamage

    def evaluateStatus(self) -> bool:
        """ updates ants status and applies status effects. Returns true if ant is still alive"""
        if self.health <= 0:
            return False
        return True
