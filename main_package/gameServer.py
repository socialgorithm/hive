import json
import uuid

from main_package.actions import Actions


class Server:

    def __init__(self):
        self.registeredPlayers = {}

    def inputFromPlayer(self, playerName: str, actionJson: str):
        action = json.loads(actionJson)
        # actions which do not require a token
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

        # check if player has valid token
        if playerName not in self.registeredPlayers:
            response = {'action': Actions.ERROR_INVALID_PLAYER, 'data': {}, 'token': None}
            self.outputToPlayer(playerName, response)
            return
        elif action['token'] != self.registeredPlayers[playerName]:
            response = {'action': Actions.ERROR_INVALID_TOKEN, 'data': {}, 'token': None}
            self.outputToPlayer(playerName, response)
            return

        # other actions
        if action['action'] == Actions.GAME_STATE:
            response = {'action': Actions.GAME_STATE, 'data': {}, 'token': None}
            self.outputToPlayer(playerName,response)
            return

    def outputToPlayer(self, playerName: str, boardStateJson: json):
        pass
