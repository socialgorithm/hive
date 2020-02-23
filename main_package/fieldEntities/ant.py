import main_package.field as field
from main_package.fieldEntities.food import Food
from main_package.interfaces.attackable import Attackable


class Ant(Attackable):

    def __init__(self, antId: str):
        Attackable.__init__(self,100)
        self.antId: str = antId
        self._maxFoodCapacity: int = 6  # how much food the ant can carry
        self.currentFood: int = 0 # how much the anti is currently carrying
        self.attackDamage: int = 1  # the damage the ant inflicts per attack
        self._foodUptakeSpeed: int = 2  # how much food the ant acquires per feed action
        self.movementEfficiency: int = 2 # TODO how many fields the ant can move before using 1 food, not yet implemented
        self.fieldPosition: field.Field = None

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

    def doAttack(self, target: Attackable):
        target.takeDamage(self.attackDamage)
