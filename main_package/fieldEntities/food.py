import main_package.field as field

class Food:

    def __init__(self, magnitude: int):
        self.foodMagnitude = magnitude
        self.fieldPosition: field.Field = None

    def getFood(self, magnitude) -> int:
        if magnitude >= self.foodMagnitude:
            returnVal = self.foodMagnitude
            self.foodMagnitude = 0
            self.fieldPosition.resetToEmpty()
            self.fieldPosition = None
            return returnVal
        else:
            self.foodMagnitude -= magnitude
            return magnitude