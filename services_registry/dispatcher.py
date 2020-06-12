"""Service Registry"""

import sys
import os
import logging
from logging.config import dictConfig
from pathlib import Path
import yaml
import json
import httpx

from aiohttp import web

from . import conf
from .validator import checker

LOG = logging.getLogger(__name__)
LOG_FILE = Path(os.getenv('SERVICES_REGISTRY_LOG', 'logger.yml')).resolve()


SERVICES = conf.services
# URLS = checker()

async def response_from_services(request):
    LOG.info('-------- response_from_services %s', request.path_qs)

    # Allow only GET and POST ?
    for name, address in SERVICES:
        url = f'{address}{request.path_qs}'
        LOG.info('%s %s', request.method, url)
        async with httpx.AsyncClient() as client:
            r = await client.request(request.method,
                                     url,
                                     # headers=request.headers,
                                     data=None if request.method == 'GET' else request.post())
            if r.status_code > 200:
                LOG.error("Invalid response [%s] for %s", r.status_code, name)
                response = f"Invalid response {r.status_code}"
            else:
                response = r.json()
                        
            yield (name, { 'request': url , 'response': response })
                

async def forward_endpoint(request):
    # if not URLS.validate(request.path_qs):
    #     LOG.error('Invalid Query %s', request.path_qs)
    #     raise web.HTTPForbidden(reason='Invalid request from whitelist/blacklist')

    LOG.info('-------- Aggregator query %s', request.path_qs)
    response = response_from_services(request)
    return web.json_response( dict([r async for r in response]) ) # change that for streaming response

async def dead(request):
    LOG.debug('deadend %s', request.path_qs)
    raise web.HTTPNotFound()

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
    server.add_routes([web.get('/favicon.ico', dead),
                       web.get('/{anything:.*}', forward_endpoint)
    ])

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
