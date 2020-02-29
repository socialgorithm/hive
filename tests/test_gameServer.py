import json
from unittest import TestCase, mock

from hive import Actions, Ant, Food, Field, FieldType, GameBoard, Server

class TestServer(TestCase):

    def setUp(self) -> None:
        self.server = Server()

    def testPlayerRegistration_uniqueAndValidName(self):
        with mock.patch.object(Server, 'outputToPlayer') as outputToPlayer:
            # register player
            jsonRegisterAction = {'action': Actions.REGISTER_PLAYER, 'data': {}}
            self.server.inputFromPlayer('testPlayerA', json.dumps(jsonRegisterAction))
            args = outputToPlayer.call_args_list[0].args
            self.assertTrue(args[1]['action'] == Actions.REGISTER_PLAYER_SUCCESS)
            self.assertTrue(args[0] == 'testPlayerA')
            self.assertTrue(args[1]['token'] is not None)

            # re-register same player
            self.server.inputFromPlayer('testPlayerA', json.dumps(jsonRegisterAction))
            args = outputToPlayer.call_args_list[1].args
            self.assertTrue(args[0] == 'testPlayerA')
            self.assertTrue(args[1]['action'] == Actions.REGISTER_PLAYER_FAILURE)
            self.assertTrue(args[1]['token'] is None)

            # register with different valid player
            self.server.inputFromPlayer('testPlayerB', json.dumps(jsonRegisterAction))
            args = outputToPlayer.call_args_list[2].args
            self.assertTrue(args[0] == 'testPlayerB')
            self.assertTrue(args[1]['action'] == Actions.REGISTER_PLAYER_SUCCESS)
            self.assertTrue(args[1]['token'] is not None)

    def testPlayerRequiresRegisteredNameAndToken(self):
        with mock.patch.object(Server, 'outputToPlayer') as outputToPlayer:

            # setup
            jsonRegisterAction = {'action': Actions.REGISTER_PLAYER, 'data': {}, 'token': None}
            someRandomAction = {'action': Actions.GAME_STATE, 'data': {}, 'token': None}
            self.server.inputFromPlayer('playerA', json.dumps(jsonRegisterAction))
            self.server.inputFromPlayer('playerB', json.dumps(jsonRegisterAction))
            tokenA = outputToPlayer.call_args_list[0].args[1]['token']
            tokenB = outputToPlayer.call_args_list[1].args[1]['token']

            # player A uses tokenA
            someRandomAction['token'] = tokenA
            self.server.inputFromPlayer('playerA', json.dumps(someRandomAction))
            args = outputToPlayer.call_args_list[2].args
            self.assertTrue(args[0] == 'playerA')
            self.assertTrue(args[1]['action'] == Actions.GAME_STATE)

            # player B uses tokenB
            someRandomAction['token'] = tokenB
            self.server.inputFromPlayer('playerB', json.dumps(someRandomAction))
            args = outputToPlayer.call_args_list[3].args
            self.assertTrue(args[0] == 'playerB')
            self.assertTrue(args[1]['action'] == Actions.GAME_STATE)

            # player A uses tokenB
            someRandomAction['token'] = tokenB
            self.server.inputFromPlayer('playerA', json.dumps(someRandomAction))
            args = outputToPlayer.call_args_list[4].args
            self.assertTrue(args[0] == 'playerA')
            self.assertTrue(args[1]['action'] == Actions.ERROR_INVALID_TOKEN)

            # player A uses token None
            someRandomAction['token'] = None
            self.server.inputFromPlayer('playerA', json.dumps(someRandomAction))
            args = outputToPlayer.call_args_list[5].args
            self.assertTrue(args[0] == 'playerA')
            self.assertTrue(args[1]['action'] == Actions.ERROR_INVALID_TOKEN)

            # player C uses token A
            someRandomAction['token'] = tokenA
            self.server.inputFromPlayer('playerC', json.dumps(someRandomAction))
            args = outputToPlayer.call_args_list[6].args
            self.assertTrue(args[0] == 'playerC')
            self.assertTrue(args[1]['action'] == Actions.ERROR_INVALID_PLAYER)
