import logging

logger = logging.getLogger('environment')


def after_scenario(context, scenario):
    logger.log(level=logging.WARN, msg="Cleanup")
    context.server.stopServer()
