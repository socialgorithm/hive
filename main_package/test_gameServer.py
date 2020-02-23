import json
from unittest import TestCase, mock

from main_package.actions import Actions
from main_package.gameBoard import gameBoard
from main_package.fieldEntities.ant import Ant
from main_package.field import FieldTypeEnum
from main_package.fieldEntities.food import Food
from main_package.gameServer import Server


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
