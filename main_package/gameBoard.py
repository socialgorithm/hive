from typing import Tuple, List, Set
from main_package.fieldEntities.ant import Ant
from main_package.field import *
from main_package.mapGenerator import *
from main_package.fieldEntities.base import Base
from main_package.fieldEntities.food import Food
from main_package.interfaces.attackable import Attackable

logging.basicConfig(level=logging.INFO)


class gameBoard:
    resolution = 5
    log = logging.getLogger(__name__)
    validForAttack = [FieldTypeEnum.ANT, FieldTypeEnum.BASE]

    def __init__(self, xdim: int = 50, ydim: int = 40):
        """
        Initializes an empty board of the given dimensions
        :param xdim: x dimension (exclusive)
        :param ydim: y dimension (exclusive)
        """
        self.xdim = xdim
        self.ydim = ydim

        mapGen = MapGenerator(xdim, ydim)
        self.gameBoard = mapGen.map
        self.ants: dict[str, Ant] = {}
        self.playerBases = {}
        self.players = []

    def getVisibleFields(self, playerName) -> List[Field] or None:
        if playerName not in self.players:
            self.log.error("Player {} is not a valid player".format(playerName))
            return None

        visibleFields: List[Field] = []
        for antId in self.getAntIdsOfPlayer(playerName):
            ant = self.getAnt(antId)
            visibleFields += self.getNeighbouringFields(ant.fieldPosition)
            visibleFields.append(ant.fieldPosition)
        base: Base = self.getBase(playerName)
        visibleFields += self.getNeighbouringFields(base.fieldPosition)
        visibleFields.append(base.fieldPosition)
        return list(set(visibleFields))

    def createBase(self, xpos: int, ypos: int, player: str) -> bool:
        # the base cannot be right at the board edge or outside the board
        if 0 >= xpos or xpos >= self.xdim or 0 >= ypos or ypos >= self.ydim:
            logging.error("Base cannot be placed outside board or at the board edge, field Dimensions {}, placement {}"
                          .format((self.xdim, self.ydim), (xpos, ypos)))
            return False

        # field where base is placed must be empty
        field = self.getField(xpos, ypos)
        if field.type != FieldTypeEnum.GRASS:
            logging.error("Base cannot be placed on field that is not grass. Field is {}".format(field.type))
            return False

        if player in self.playerBases.keys():
            logging.error("Player " + player + " already has a base")
            return False

        # placing base
        base = Base(player)
        field.setEntity(base)
        self.playerBases[player] = base
        self.players.append(player)
        self.log.info("base for player {} created at coordinates ({},{})".format(player,xpos,ypos))
        return True

    def getBoardString(self):
        boardString = ""
        for y in range(len(self.gameBoard)):
            yRow = self.gameBoard[y]
            for x in range(len(yRow)):
                field = yRow[x]
                boardString += " " + str(field) + " "
            boardString += "\n"
        return boardString

    def getField(self, x: int, y: int):
        if not 0 <= x < self.xdim or not 0 <= y < self.ydim:
            self.log.error("Invalid board position {}".format((x, y)))
            return None
        return self.gameBoard[y][x]

    def getNeighbouringFieldCoordinates(self, xpos, ypos) -> List[Tuple]:
        neighbouringFieldCoords = []
        for y_offset in [-1, 0, 1]:
            for x_offset in [-1, 0, 1]:
                if x_offset == y_offset == 0:
                    continue  # ignoring centre field, we want neighbours
                xcoord = xpos + x_offset
                ycoord = ypos + y_offset
                if 0 <= xcoord < self.xdim and 0 <= ycoord < self.ydim:
                    coords = (xcoord, ycoord)
                    neighbouringFieldCoords.append(coords)
        return neighbouringFieldCoords

    def getNeighbouringFields(self, field) -> List:
        assert (isinstance(field, Field))
        neighbours = []
        for coords in self.getNeighbouringFieldCoordinates(field.xpos, field.ypos):
            neighbour = self.getField(coords[0], coords[1])
            if neighbour is not None:
                neighbours.append(neighbour)
        return neighbours

    def getAntIdsOfPlayer(self, playerName: str) -> List[str] or None:
        if playerName not in self.players:
            self.log.error("Player {} is not a valid player".format(playerName))
            return None
        playersAnts = list(filter(lambda ant: ant.playerName == playerName, self.ants.values()))
        return list(map(lambda ant: ant.antId, playersAnts))

    def createAnt(self, xpos: int, ypos: int, antId: str, player: str) -> bool:

        # TODO player can only create ants in sections visible to them
        # check if an ant with this id already exists
        antId = str.lower(antId)
        if self.getAnt(antId) is not None:
            self.log.error("Ant with id {} already exists".format(antId))
            return False

        # check if in board
        if not 0 <= xpos < self.xdim or not 0 <= ypos < self.ydim:
            self.log.error("position " + (xpos, ypos) + " is outside of the board dimensions " + (self.xdim, self.ydim))
            return False

        # placement checks
        placementDesitnation: Field = self.getField(xpos, ypos)
        neighbouring_fields: List[Field] = self.getNeighbouringFields(placementDesitnation)
        if not any(f.type == FieldTypeEnum.BASE for f in neighbouring_fields):
            self.log.error("Invalid Placement, no adjacent base")
            return False
        elif placementDesitnation.type is not FieldTypeEnum.GRASS:
            self.log.error("Invalid Placement, field not grass")
            return False

        # check if player owns base near which they want to place ant
        base: Base = next(filter(lambda x: x.type == FieldTypeEnum.BASE, neighbouring_fields)).entity
        if base.player != player:
            self.log.error("Player {} does not own the adjacent base".format(player))
            return False

        # set field to ant
        self.ants[antId] = Ant(antId, player)
        placementDesitnation.setEntity(self.ants[antId])
        self.log.info("Ant with id {} created at position ({},{})"
                      .format(antId, placementDesitnation.xpos, placementDesitnation.ypos))
        return True

    def moveAnt(self, antId: str, xpos: int, ypos: int) -> bool:
        antId = str.lower(antId)

        # ensure that antId is valid
        if self.getAnt(antId) is None:
            return False
        ant = self.ants[antId]
        # determine valid fields for movement
        fields = self.getNeighbouringFields(ant.fieldPosition)
        validFields = filter(lambda x: x.type != FieldTypeEnum.ROCK, fields)

        # is movement valid ?
        fieldToMoveTo: Field = None
        for field in validFields:
            if field.xpos == xpos and field.ypos == ypos:
                fieldToMoveTo = field
                break
        currentx = ant.fieldPosition.xpos
        currenty = ant.fieldPosition.ypos
        if fieldToMoveTo is None:
            self.log.error("Movement of antId={} ({},{})->({},{}) is not valid.".format(
                ant.antId, currentx, currenty, xpos, ypos))
            return False

        # do move
        ant.fieldPosition.resetToEmpty()  # reset old field
        fieldToMoveTo.setEntity(ant)
        self.log.info("Ant antId={} moved ({},{})->({},{}) ".format(ant.antId, currentx, currenty, xpos, ypos))
        return True

    def attack(self, antId: str, xpos: int, ypos: int) -> bool:
        antId = str.lower(antId)
        # ensure that antId is valid
        attackingAnt = self.getAnt(antId)
        if attackingAnt is None:
            return False
        # ensure target is valid
        neighbouringFields = self.getNeighbouringFields(attackingAnt.fieldPosition)
        fieldToAttack = self.getField(xpos, ypos)
        if fieldToAttack not in neighbouringFields:
            self.log.error("The field {} is not in range of ant {}".format((xpos, ypos), antId))
            return False
        if fieldToAttack.type not in gameBoard.validForAttack:
            self.log.error("The field {} is not a valid attack target for ant {}".format((xpos, ypos), antId))
            return False
        target: Attackable = fieldToAttack.entity  # TODO: might need "attackable" interface later
        attackingAnt.doAttack(target)
        return True

    def tick(self):
        """ tick checks status of all ants ant takes required actions accordingly (e.g remove ants with health < 1)"""
        antsToRemove: [str] = []
        for (antId, entity) in self.ants.items():
            if entity.isDead(): antsToRemove.append(antId)
        for antId in antsToRemove:
            deadAnt: Ant = self.ants[antId]
            self.log.info("Ant {} Killed !".format(deadAnt.antId))
            deadAnt.fieldPosition.resetToEmpty()
            del self.ants[antId]
        """ remove destroyed bases"""
        basesToRemove: [str] = []
        for (playerName, entity) in self.playerBases.items():
            if entity.isDead(): basesToRemove.append(playerName)
        for playerName in basesToRemove:
            destroyedBase: Base = self.playerBases[playerName]
            self.log.info("Base of player {} destroyed !".format(destroyedBase.player))
            destroyedBase.fieldPosition.resetToEmpty()
            del self.playerBases[playerName]

    def getAnt(self, antId: str) -> Ant or None:
        antId = str.lower(antId)
        if antId not in self.ants.keys():
            self.log.error("No ant with id: {}".format(antId))
            return None
        return self.ants[antId]

    def getBase(self, playerName: str) -> Base or None:
        if playerName not in self.playerBases.keys():
            self.log.error("Player {} has no base".format(playerName))
            return None
        return self.playerBases[playerName]

    def createFood(self, xpos: int, ypos: int, magnitude: int) -> bool:
        targetField = self.getField(xpos, ypos)
        if targetField is None or targetField.type is not FieldTypeEnum.GRASS:
            self.log.error("Invalid target ({},{}) for placing food.".format(xpos, ypos))
            return False
        if magnitude <= 0 or magnitude != magnitude:  # test for negative or nan
            self.log.error("Invalid food magnitude value {}".format(magnitude))
            return False
        foodEntity = food.Food(magnitude)
        targetField.setEntity(foodEntity)
        return True

    def feed(self, antId: str, targetXpos: int, targetYpos: int) -> bool:
        # checking if an ant with the given id exists
        if self.getAnt(antId) is None:
            self.log.error("No ant with Id {}".format(antId))
            return False
        feedingAnt: Ant = self.getAnt(antId)
        targetField = self.getField(targetXpos, targetYpos)
        # check if ant is next to food field
        if targetField not in self.getNeighbouringFields(feedingAnt.fieldPosition):
            self.log.error("Ant with id {} is not in range of targeted field ({},{})".format(antId, targetXpos, targetYpos))
            return False
        # check if field is food
        if targetField.type != FieldTypeEnum.FOOD:
            self.log.error("Ant with id {} tried to feed on a non food field ({},{})".format(antId,targetXpos,targetYpos))
            return False
        # ants have a food capacity and feeding speed value
        foodEntity: Food = targetField.entity
        return feedingAnt.feed(foodEntity)

