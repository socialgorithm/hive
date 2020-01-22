import logging
from typing import Tuple, List
from main_package.field import *
logging.basicConfig(level=logging.INFO)

class hiveServer:
    log = logging.getLogger(__name__)

    def __init__(self, xdim: int=10, ydim:int=10):
        self.xdim = xdim
        self.ydim = ydim
        self.gameBoard = [[Field(xpos=x, ypos=y) for x in range(xdim)] for y in range(ydim)]
        self.getField(xdim-2, 1).type = FieldTypeEnum.BASE  # player 1 base
        self.getField(1, ydim-2).type = FieldTypeEnum.BASE  # player 2 base


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
            self.log.error("Invalid board position " + (x, y))
            return None
        return self.gameBoard[y][x]

    def getNeighbouringFields(self, field) -> List:
        assert(isinstance(field, Field))
        neighbours = []
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if x_offset == y_offset == 0:
                    continue  # ignoring centre field, we want neighbours
                neighbour = self.getField(field.xpos+x_offset, field.ypos+y_offset)
                if neighbour is not None:
                    neighbours.append(neighbour)
        return neighbours


    def createAnt(self, xpos: int, ypos: int) -> bool:
        # check if in board
        if not 0 <= xpos < self.xdim or not 0 <= ypos < self.ydim:
            self.log.error("position " + (xpos, ypos) + " is outside of the board dimensions " + (self.xdim, self.ydim))
            return False

        placement_desitnation = self.gameBoard[ypos][xpos]
        # placement checks
        neighbouring_fields: List[Field] = self.getNeighbouringFields(placement_desitnation)
        if not any(f.type == FieldTypeEnum.BASE for f in neighbouring_fields):
            self.log.error("Invalid Placement, no adjacent base")
            return False
        elif placement_desitnation.type is not FieldTypeEnum.EMPTY:
            self.log.error("Invalid Placement, field not empty")
            return False
        placement_desitnation.type = FieldTypeEnum.ANT
        return True
