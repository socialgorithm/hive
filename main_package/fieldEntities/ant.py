import main_package.field as field
from main_package.fieldEntities.food import Food
from main_package.interfaces.Entity import Entity, EntityType
from main_package.interfaces.attackable import Attackable


class Ant(Entity, Attackable):

    def __init__(self, antId: str, playerName: str):
        Entity.__init__(self, antId, playerName, EntityType.ANT)
        Attackable.__init__(self, 100)
        self.antId: str = antId
        self.playerName = playerName
        self._maxFoodCapacity: int = 6  # how much food the ant can carry
        self.currentFood: int = 0 # how much the anti is currently carrying
        self.attackDamage: int = 1  # the damage the ant inflicts per attack
        self._foodUptakeSpeed: int = 2  # how much food the ant acquires per feed action
        self.fieldPosition: field.Field = None

    def getAntDetailedInfo(self):
        info = {
            "maxFoodCapacity": self._maxFoodCapacity,
            "currentFood": self.currentFood,
            "attackDamage": self.attackDamage,
            "foodUptakeSpeed": self._foodUptakeSpeed,
        }
        return info

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
        obtainedFood = food.takeFood(self.getFoodUptakeValue())
        self.currentFood += obtainedFood
        return obtainedFood > 0

    def doAttack(self, target: Attackable):
        target.takeDamage(self.attackDamage)
