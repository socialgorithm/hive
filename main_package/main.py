from main_package.gameBoard import gameBoard
import sys

if __name__ == '__main__':
    print(sys.path)
    server = gameBoard()
    print(server.getBoardString())