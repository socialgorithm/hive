from .world import GameBoard
import sys

if __name__ == '__main__':
    print(sys.path)
    server = GameBoard()
    print(server.getBoardString())