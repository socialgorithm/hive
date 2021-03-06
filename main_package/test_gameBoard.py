from typing import List
from unittest import TestCase

from main_package.fieldEntities.base import Base
from main_package.gameBoard import gameBoard
from main_package.fieldEntities.ant import Ant
from main_package.field import FieldTypeEnum, Field
from main_package.fieldEntities.food import Food


class TestgameBoard(TestCase):
    """
              0   1   2   3   4   5
            -------------------------
        0   |   |   |a2 |   |   |   |
            -------------------------
        1   |   |P1 |   |b1 |P2 |b2 |
            -------------------------
        2   |a1 |   | F |   |   |   |
            -------------------------
        3   |   |   |   |c1 |   |   |
            -------------------------
        4   |   |   |   |   |P3 |   |
            -------------------------
        5   |   |   |   |   |   |   |
            """

    def test_getPlayerGameState_eachPlayerOnlySeesTheirStuff(self):
        # setup
        board = gameBoard(6, 6)
        board.createBase(1, 1, "player1")
        board.createBase(4, 1, "player2")
        board.createBase(4, 4, "player3")
        board.createAnt(0, 2, "a1", "player1")
        board.createAnt(2, 0, "a2", "player1")
        board.createAnt(3, 1, "b1", "player2")
        board.createAnt(5, 1, "b2", "player2")
        board.createAnt(3, 3, "c1", "player3")
        board.createFood(2, 2, 59)

        statePlayer1 = board.getPlayerGameState("player1")
        statePlayer2 = board.getPlayerGameState("player2")
        statePlayer3 = board.getPlayerGameState("player3")

        # player1 sees some of player2's assets & food, but nothing from player 3
        self.assertTrue(all(elem in statePlayer1["visibleEntities"]["ants"].keys() for elem in ["a1", "a2"]))
        self.assertTrue(all(elem in statePlayer1["visibleEntities"]["ants"].keys() for elem in ["b1"]))
        self.assertTrue(not any(elem in statePlayer1["visibleEntities"]["ants"].keys() for elem in ["c1", "b2"]))
        self.assertTrue(len(statePlayer1["visibleEntities"]["food"].keys()) == 1)
        self.assertTrue(statePlayer1["visibleEntities"]["food"][next(iter(statePlayer1["visibleEntities"]["food"]))]["quantity"] == 59)

        # player2 sees some of player1's assets & food, but nothing from player 3
        self.assertTrue(all(elem in statePlayer2["visibleEntities"]["ants"].keys() for elem in ["b1", "b2", "a2"]))
        self.assertTrue(not any(elem in statePlayer2["visibleEntities"]["ants"].keys() for elem in ["c1", "a1"]))
        self.assertTrue(len(statePlayer2["visibleEntities"]["food"].keys()) == 1)
        self.assertTrue(statePlayer2["visibleEntities"]["food"][next(iter(statePlayer2["visibleEntities"]["food"]))][
                            "quantity"] == 59)

        # player 1 sees detail about own ants but not about the ants of other players
        self.assertTrue(len(statePlayer1["visibleEntities"]["ants"]["a1"]["detailedInfo"].keys()) > 0)
        self.assertTrue(len(statePlayer1["visibleEntities"]["ants"]["a2"]["detailedInfo"].keys()) > 0)
        self.assertTrue(len(statePlayer1["visibleEntities"]["ants"]["b1"]["detailedInfo"].keys()) == 0)


    def test_fogOfWar(self):
        # setup
        board = gameBoard(6, 6)
        board.createBase(1,1,"player1")
        board.createBase(4,4,"player2")
        board.createAnt(2,1,"a","player1")
        board.createAnt(3,4,"b","player2")

        # test that invalid player name yields None
        self.assertTrue(board.getVisibleFields("invalid") is None)

        # check p1 visible fields
        visibleFieldsP1: List[Field] = board.getVisibleFields("player1")
        expectedVisibleFieldsP1 = [(x, y) for x in range(0, 4) for y in range(0, 3)]
        self.assertTrue(all(visible.getPos() in expectedVisibleFieldsP1 for visible in visibleFieldsP1))
        self.assertTrue(len(visibleFieldsP1) == len(expectedVisibleFieldsP1))

        # check p2 visible fields
        visibleFieldsP2: List[Field] = board.getVisibleFields("player2")
        expectedVisibleFieldsP2 = [(x, y) for x in range(2, 6) for y in range(3, 6)]
        self.assertTrue(all(visible.getPos() in expectedVisibleFieldsP2 for visible in visibleFieldsP2))
        self.assertTrue(len(visibleFieldsP1) == len(expectedVisibleFieldsP1))

        # move ant and check that visible fields correctly updates
        board.moveAnt("b", 3, 3)
        board.moveAnt("b", 3, 2)
        visibleFieldsP2: List[Field] = board.getVisibleFields("player2")
        expectedVisibleFieldsP2 = list(set([(x, y) for x in range(2, 5) for y in range(1, 4)] + [(x, y) for x in range(3, 6) for y in range(3, 6)]))
        self.assertTrue(all(visible.getPos() in expectedVisibleFieldsP2 for visible in visibleFieldsP2))
        self.assertTrue(len(visibleFieldsP2) == len(expectedVisibleFieldsP2))
        visibleFieldsP1: List[Field] = board.getVisibleFields("player1")
        expectedVisibleFieldsP1 = [(x, y) for x in range(0, 5) for y in range(0, 3)]  # player 1 visibility unchanged
        self.assertTrue(all(visible.getPos() in expectedVisibleFieldsP1 for visible in visibleFieldsP1))

    def test_ant_creation(self):
        board = gameBoard(10, 10)
        board.createBase(2, 2, "testPlayer")
        # cant create ant with invalid player name
        self.assertFalse(board.createAnt(1, 1, "someAnt", "otherPlayer"))
        board.createBase(6, 6, "otherPlayer")
        self.assertTrue(board.createAnt(6, 7, "someAnt", "otherPlayer"))
        # ant has to be placed next to base
        self.assertTrue(board.createAnt(2, 3, "A", "testPlayer"))
        self.assertFalse(board.createAnt(4, 4, "B", "testPlayer"))  # not next to base
        # cant place ant on-top of another ant
        self.assertFalse(board.createAnt(2, 3, "C", "testPlayer"))
        # cant create two ants with same ID
        self.assertFalse(board.createAnt(1, 2, "A", "testPlayer"))

    def test_base_creation(self):
        board = gameBoard(10, 10)
        self.assertTrue(board.createBase(2, 2, "testPlayer"))
        self.assertFalse(board.createBase(2, 2, "testPlayer2"))  # base already exists at same coords
        self.assertFalse(board.createBase(15, 15, "testPlayer3"))  # outside board
        self.assertFalse(board.createBase(0, 0, "testPlayer4"))  # at board edge
        self.assertFalse(board.createBase(3, 3, "testPlayer"))  # valid coords but 'testPlayer' already has a base

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
        board.createAnt(0, 0, "A", "testPlayer")
        board.createAnt(0, 1, "B", "testPlayer")
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
        board.createAnt(0, 0, "A", "testPlayer")
        board.createAnt(0, 1, "B", "testPlayer")
        board.createAnt(0, 2, "C", "testPlayer")
        self.assertFalse(board.attack("A", 0, 2))  # attacking out of reach ant
        self.assertFalse(board.attack("A", -1, 0))  # attacking field outside of board
        self.assertFalse(board.attack("A", 0, 0))  # cant self harm
        print(board.getBoardString())

        # testing killing of another ant
        antA: Ant = board.getAnt("A")
        antA.attackDamage = 5
        antB: Ant = board.getAnt("B")
        antBField = antB.fieldPosition
        self.assertTrue(antBField.type == FieldTypeEnum.ANT)
        antB.health = 10
        self.assertTrue(board.attack("A", 0, 1))
        self.assertTrue(antB.health == 5)
        board.tick()
        self.assertTrue(antBField.type == FieldTypeEnum.ANT)
        self.assertTrue(board.getAnt("B") is not None)  # ant C damaged but alive
        self.assertTrue(board.attack("A", 0, 1))
        self.assertTrue(antB.health == 0)
        board.tick()
        self.assertTrue(antBField.type == FieldTypeEnum.EMPTY)
        self.assertTrue(board.getAnt("B") is None)  # dead ants removed from board

        # test attacking and killing base
        base: Base = board.getBase("testPlayer")
        baseField = base.fieldPosition
        self.assertTrue(baseField.type == FieldTypeEnum.BASE)
        base.health = 10
        self.assertTrue(board.attack("A", 1, 1))
        board.tick()
        self.assertTrue(base.health == 5)
        self.assertTrue(board.attack("A", 1, 1))
        board.tick()
        self.assertTrue(baseField.type == FieldTypeEnum.EMPTY)
        self.assertTrue(board.getBase("testPlayer") is None)
        base.health = 0


    def test_ant_feed(self):
        board = gameBoard(5, 5)
        board.createBase(1, 1, "testPlayer")
        board.createAnt(0, 1, "A", "testPlayer")
        antA: Ant = board.getAnt("A")
        board.createAnt(1, 2, "B", "testPlayer")
        board.createAnt(0, 2, "C", "testPlayer")
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
        self.assertFalse(board.feed("B", 0, 3))  # ant is full
        self.assertTrue(food.foodMagnitude == 5)
        self.assertTrue(antB.currentFood == 6)
        # C feed, check food status
        self.assertTrue(board.feed("C", 0, 3))
        self.assertTrue(board.feed("C", 0, 3))
        self.assertTrue(board.feed("C", 0, 3))
        self.assertFalse(board.feed("C", 0, 3))  # food source empty
        self.assertTrue(antC.currentFood == 5)
        self.assertTrue(board.getField(0, 3).type == FieldTypeEnum.EMPTY)  # check food source depleation

    def test_getAntIdsOfPlayer(self):
        board = gameBoard(5, 5)
        board.createBase(1, 1, "player1")
        board.createAnt(0, 1, "a1", "player1")
        board.createAnt(0, 0, "a2", "player1")
        board.createAnt(0, 2, "a3", "player1")
        board.createBase(3, 3, "player2")
        board.createAnt(4, 3, "b1", "player2")
        board.createAnt(2, 3, "b2", "player2")
        self.assertTrue(all(elem in board.getAntIdsOfPlayer("player1") for elem in ["a1", "a2", "a3"]))
        self.assertTrue(all(elem in board.getAntIdsOfPlayer("player2") for elem in ["b1", "b2"]))
        self.assertTrue(not any(elem in board.getAntIdsOfPlayer("player2") for elem in ["a1", "a2", "a3"]))
        self.assertTrue(not any(elem in board.getAntIdsOfPlayer("player1") for elem in ["b1", "b2"]))

        # test that method call with invalid player name yields None
        self.assertTrue(board.getAntIdsOfPlayer("invalid") is None)
