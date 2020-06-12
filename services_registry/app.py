"""Service Registry"""

import sys
import os
import logging
from logging.config import dictConfig
from pathlib import Path
import yaml

from aiohttp import web

from . import conf
from .validator import validator

LOG = logging.getLogger(__name__)
LOG_FILE = Path(os.getenv('SERVICES_REGISTRY_LOG', 'logger.yml')).resolve()


def main(path=None):

    # Configure basic logging
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    # Configure more logging, if found
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as stream:
            dictConfig(yaml.safe_load(stream))

    # Create the server
    server = web.Application()

    # Add the routes
    server.add_routes(validator.routes)

    # .... and cue music!
    LOG.info(f"Start services registry")
    # .... and cue music
    if path:
        if os.path.exists(path):
            os.unlink(path)
        # will create the UDS socket and bind to it
        web.run_app(server,
                    path=path,
                    shutdown_timeout=0,
                    ssl_context=getattr(conf, 'ssl_context', None))
    else:
        web.run_app(server,
                    host=getattr(conf, 'host', '0.0.0.0'),
                    port=getattr(conf, 'port', 8000),
                    shutdown_timeout=0,
                    ssl_context=getattr(conf, 'ssl_context', None))
