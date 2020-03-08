import main_package.field as field
from main_package.interfaces.Entity import Entity, EntityType


class Food(Entity):

    def __init__(self, magnitude: int):
        Entity.__init__(self, self.__hash__().__str__(), "", EntityType.FOOD)  # TODO do food entities need an ID value ?
        self.foodMagnitude = magnitude
        self.fieldPosition: field.Field = None

    def getRemainingFoodQuantity(self) -> int:
        return self.foodMagnitude

    def takeFood(self, magnitude) -> int:
        """
        Reduces the amount of food held by this entity
        :param magnitude:
        :return:
        """
        if magnitude >= self.foodMagnitude:
            returnVal = self.foodMagnitude
            self.foodMagnitude = 0
            self.fieldPosition.resetToEmpty()
            self.fieldPosition = None
            return returnVal
        else:
            self.foodMagnitude -= magnitude
            return magnitude