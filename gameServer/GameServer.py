import logging
import threading
from urllib import parse
import socketio
import eventlet


class Server(socketio.Namespace,threading.Thread):

    logger = logging.getLogger('Server')
    gameInfo = "Hive Game!"

    def __init__(self, url: str, port: int):
        print('STARTING SERVER @ {}:{}'.format(url,port))
        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(self.sio)
        self.playerToSocket = {}
        self.tournamentServerSessionId = "";
        self.sio.on('connect', self.connect)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('CreateMatch', self.createMatch)

        # thread
        self.thread : threading.Thread = threading.Thread(target=self.startServer, args=(self.app, url, port))
        self.thread.daemon = True
        self.thread.start()

    def stopServer(self):
        logging.log(level=logging.WARN, msg="Killing server")
        eventlet.kill

    def startServer(self, _app, _url, _port):
        eventlet.wsgi.server(eventlet.listen((_url, _port)), _app)

    def connect(self, sid, environ):

        # extracting player token and creating mapping: token -> session id
        try:
            token = parse.parse_qs(environ['QUERY_STRING'])['token'][0]
        except KeyError:
            message = "Failed to get token from query string {query}. sid:{sid}, assuming its the tournament server".format(sid=sid, query=environ['QUERY_STRING'])
            logging.log(level=logging.WARN, msg=message)

        if token is not None:
            self.playerToSocket[token] = sid
            self.onPlayerConnected(sid)
        else:
            self.onTournamentServerConnected(sid)

    def disconnect(self, sid):
        print('disconnect ', sid)

    def onPlayerConnected(self, sid):
        pass

    def onTournamentServerConnected(self, sid):
        self.tournamentServerSessionId = sid
        self.sio.emit(event="GameInfo", data=self.gameInfo, to=sid)

    def createMatch(self, sid):
        if sid != self.tournamentServerSessionId:
            self.sio.send(data="FORBIDDEN! you are not the tournament server.", to=sid)
            return

