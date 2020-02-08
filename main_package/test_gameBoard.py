from unittest import TestCase
from main_package.gameBoard import gameBoard
from main_package.fieldEntities.ant import Ant
from main_package.field import FieldTypeEnum
from main_package.fieldEntities.food import Food

class TestgameBoard(TestCase):

    def test_ant_creation(self):
        board = gameBoard(10, 10)
        board.createBase(2, 2, "testPlayer")
        # ant has to be placed next to base
        self.assertTrue(board.createAnt(2, 3, "A"))
        self.assertFalse(board.createAnt(4, 4, "B"))  # not next to base
        # cant place ant on-top of another ant
        self.assertFalse(board.createAnt(2, 3, "C"))
        # cant create two ants with same ID
        self.assertFalse(board.createAnt(1, 2, "A"))

    def test_base_creation(self):
        board = gameBoard(10, 10)
        self.assertTrue(board.createBase(2, 2, "testPlayer"))
        self.assertFalse(board.createBase(2, 2, "testPlayer"))
        self.assertFalse(board.createBase(15, 15, "testPlayer"))  # outside board
        self.assertFalse(board.createBase(0, 0, "testPlayer"))  # at board edge

    def test_get_neighbouring_field_coordinates(self):
        board = gameBoard(3, 3)
        coords = board.getNeighbouringFieldCoordinates(1, 1)  # middle of board
        self.assertTrue(len(coords) == 8)
        for coordinate in [(0, 0), (0, 1), (0, 2), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]:
            self.assertTrue(coordinate in coords)
        # now testing that the method does not return invalid coordinates (e.g. outside of board)
        coords = board.getNeighbouringFieldCoordinates(2, 0)  # top left edge of board
        self.assertTrue(len(coords) == 3)
        for coordinate in [(1, 0), (1, 1), (2, 1)]:
            self.assertTrue(coordinate in coords)

    def test_ant_movement(self):
        board = gameBoard(4, 4)
        board.createBase(1, 1, "testPlayer")
        board.createAnt(0, 0, "A")
        board.createAnt(0, 1, "B")
        self.assertFalse(board.moveAnt("A", 0, 1))  # move to occupied field
        self.assertTrue(board.moveAnt("B", 0, 2))  # move to empty field
        self.assertTrue(board.moveAnt("A", 0, 1))  # move to previously occupied field
        self.assertFalse(board.moveAnt("A", 0, 1))  # move to current field
        self.assertFalse(board.moveAnt("B", -1, 2))  # move to field outside board
        self.assertFalse(board.moveAnt("A", 2, 1))  # move to empty but out of range field
        self.assertTrue(board.moveAnt("A", 0, 0))  # move to previous field
        self.assertTrue(board.moveAnt("B", 1, 3))  # diagonal movement
        self.assertFalse(board.moveAnt("C", 1, 3))  # moving ant that does not exist

    def test_ant_attack(self):
        board = gameBoard(3, 3)
        board.createBase(1, 1, "testPlayer")
        board.createAnt(0, 0, "A")
        board.createAnt(0, 1, "B")
        board.createAnt(0, 2, "C")
        self.assertFalse(board.attack("A", 0, 2))  # attacking out of reach ant
        self.assertFalse(board.attack("A", -1, 0))  # attacking field outside of board
        self.assertFalse(board.attack("A", 0, 0))  # cant self harm
        print(board.getBoardString())
        # testing killing of another ant
        antA: Ant = board.getAnt("A")
        antA.attackDamage = 5
        antC: Ant = board.getAnt("B")
        antC.health = 10
        self.assertTrue(board.attack("A", 0, 1))
        self.assertTrue(antC.health == 5)
        board.tick()
        self.assertTrue(board.getAnt("B") is not None)  # ant C damaged but alive
        self.assertTrue(board.attack("A", 0, 1))
        self.assertTrue(antC.health == 0)
        board.tick()
        self.assertTrue(board.getAnt("B") is None)  # dead ants removed from board

    def test_ant_feed(self):
        board = gameBoard(5, 5)
        board.createBase(1, 1, "testPlayer")
        board.createAnt(0, 1, "A")
        antA: Ant = board.getAnt("A")
        board.createAnt(1, 2, "B")
        board.createAnt(0, 2, "C")
        antC: Ant = board.getAnt("C")
        antB: Ant = board.getAnt("B")
        self.assertTrue(board.createFood(0, 3, 11))
        self.assertTrue(board.getField(0, 3).type == FieldTypeEnum.FOOD)
        # feeding out of range
        food: Food = board.getField(0, 3).entity
        self.assertFalse(board.feed("A", 0, 3))
        self.assertTrue(food.foodMagnitude == 11)
        self.assertTrue(antA.currentFood == 0)
        # ant B is in range and should be able to feed
        self.assertTrue(board.feed("B", 0, 3))
        self.assertTrue(food.foodMagnitude == 9)
        self.assertTrue(antB.currentFood == 2)
        # fill ant B
        self.assertTrue(board.feed("B", 0, 3))
        self.assertTrue(board.feed("B", 0, 3))
        self.assertFalse(board.feed("B", 0, 3)) # ant is full
        self.assertTrue(food.foodMagnitude == 5)
        self.assertTrue(antB.currentFood == 6)
        # C feed, check food status
        self.assertTrue(board.feed("C", 0, 3))
        self.assertTrue(board.feed("C", 0, 3))
        self.assertTrue(board.feed("C", 0, 3))
        self.assertFalse(board.feed("C", 0, 3)) # food source empty
        self.assertTrue(antC.currentFood == 5)
        self.assertTrue(board.getField(0, 3).type == FieldTypeEnum.EMPTY) # check food source depleation