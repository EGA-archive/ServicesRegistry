"""Service Registry"""

import sys
import os
import logging
from pathlib import Path
import yaml

from aiohttp import web

from . import conf, endpoints

LOG = logging.getLogger(__name__)

# Configure more logging, if found
LOG_FILE = Path(__file__).parent / "logger.yml"
if LOG_FILE.exists():
    from logging.config import dictConfig
    with open(LOG_FILE, 'r') as stream:
        dictConfig(yaml.safe_load(stream))

def main(path=None):

    # Create the server
    server = web.Application()

    # Add the routes
    server.add_routes(endpoints.routes)

    # .... and cue music!
    LOG.info(f"Start services registry")
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
