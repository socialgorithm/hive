import socketio


class SockClient:

    def __init__(self, url: str):
        self.sio = socketio.Client()
        self.sio.on('connect', self.connect)
        self.sio.connect(url)

    def connect(self):
        print('client connected')
