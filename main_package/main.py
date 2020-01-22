from main_package.hiveServer import hiveServer
import sys

if __name__ == '__main__':
    print(sys.path)
    server = hiveServer()
    server.createAnt(7,1)
    server.createAnt(7,2)
    server.createAnt(2,7)
    print(server.getBoardString())