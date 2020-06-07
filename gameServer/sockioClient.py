import socketio


class SockClient:

    def __init__(self, url: str):
        self.sio = socketio.Client()
        self.sio.on('connect', self.connect)
        self.sio.on('GameInfo', self.gameInfo)
        self.receivedGameInfo = ''
        self.sio.connect(url)

    def connect(self):
        print('client connected')

    def gameInfo(self, data):
        self.receivedGameInfo = data
        print('Game Info:'.format(data))
