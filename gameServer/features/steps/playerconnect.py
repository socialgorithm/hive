import logging

from behave import *

from gameServer.GameServer import Server

logger = logging.getLogger('playerconnect.feature')
from gameServer.sockioClient import SockClient


@given('the server is listening on {url} port {port:d}')
def step_impl(context, url, port):
    context.playerToSocket = {}
    context.server = Server(url, port)


@given('entity "{entity}" connects to "{url}"')
def step_impl(context, entity, url):
    try:
        setattr(context, entity, SockClient(url))
    except:
        logger.log(logging.INFO, 'Connection refused')


@then('player with token "{playerToken}" has connected')
def step_impl(context, playerToken):
    print(context.server.playerToSocket)
    assert (context.server.playerToSocket[playerToken] is not None)


@then('{num:d} players have connected')
def step_impl(context, num):
    print(context.server.playerToSocket)
    assert (len(context.server.playerToSocket) == num)


@then('entity "{entity}" has field "{field}" with value "{value}"')
def step_impl(context,entity,field,value):
    print(context.tournamentServer)
    entity = getattr(context,entity)
    entityField = getattr(entity,field)
    assert(entityField == value)