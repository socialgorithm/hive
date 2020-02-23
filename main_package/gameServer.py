import json
import uuid

from main_package.actions import Actions


class Server:

    def __init__(self):
        self.registeredPlayers = {}

    def inputFromPlayer(self, playerName: str, actionJson: str):
        action = json.loads(actionJson)
        if action['action'] == Actions.REGISTER_PLAYER:
            # ensure that player is not already registered
            if playerName in self.registeredPlayers.keys():
                response = {'action': Actions.REGISTER_PLAYER_FAILURE, 'data': {}, 'token': None}
                self.outputToPlayer(playerName, response)
                return
            # carry out registration
            playerToken = str(uuid.uuid4())  # for the player to send with actions to authenticate
            response = {'action': Actions.REGISTER_PLAYER_SUCCESS, 'data': {}, 'token': playerToken}
            self.registeredPlayers[playerName] = playerToken
            self.outputToPlayer(playerName, response)
            return

    def outputToPlayer(self, playerName: str, boardStateJson: json):
        pass
