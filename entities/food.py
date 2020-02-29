
class Food:

    def __init__(self, magnitude: int):
        self.foodMagnitude = magnitude

    def getFood(self, magnitude) -> int:
        if magnitude >= self.foodMagnitude:
            returnVal = self.foodMagnitude
            self.foodMagnitude = 0
            return returnVal
        else:
            self.foodMagnitude -= magnitude
            return magnitude