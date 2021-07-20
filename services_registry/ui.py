"""Service Registry"""

import sys
import os
import logging
from logging.config import dictConfig
from pathlib import Path
import asyncio
from urllib.parse import quote
import json

import yaml
from aiohttp import web
import aiohttp_jinja2
import jinja2

from . import conf

from .utils import Collector, explore_service
from .endpoints import dispatcher

LOG = logging.getLogger(__name__)
LOG_FILE = Path(os.getenv('SERVICES_REGISTRY_LOG', 'logger.yml')).resolve()

collector = Collector(conf.services)

async def initialize(app):
    """Initialize HTTP server."""
    templates_path = Path(__file__).parent.parent / 'templates'
    LOG.debug('template directory: %s', str(templates_path))
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(str(templates_path)))
    app['static_root_url'] = '/static'
    LOG.info("Initialization done.")


@aiohttp_jinja2.template('index.html')
async def index(request):
    results = await collector.request('GET', '', json=True)
    #LOG.debug('results: %s', results)
    services_info = [explore_service(*args) for args in results]
    return {
        "services": services_info,
        "service_title": getattr(conf, 'service_title', ''),
        "service_logos": getattr(conf, 'service_logos', None)
    }

async def dispatch(request):
    data = await request.post()
    LOG.debug('Captured data: %s', data)
    url = data.get('url', '')
    if not url or url[0] != '/':
        url = '/' + url
    LOG.debug('Captured URL: %s', url)
    raise web.HTTPFound(url)
    # redirect = quote(url)
    # LOG.info('Redirect to: %s', redirect)
    # raise web.HTTPFound(redirect)

    # results = await collector.request(request.method,
    #                                   path,
    #                                   headers=request.headers,
    #                                   data=data,
    #                                   json=json)
    # responses = {}
    # for (name, url, response, error) in results:
    #     if response: # and not error
    #         responses[name] = {'request': request.method + ' ' + url, 'response': response }
    #     else:
    #         responses[name] = {'request': request.method + ' ' + url, 'error': error }

    # LOG.info('-------- Aggregator query %s | responses %d', request.path_qs, len(responses))
    # # d = json.dumps(responses)
    # # LOG.info('-------- sending %s', d)
    # # return web.Response(text=d, content_type='application/json')
    # return web.json_response(responses)  # change that for streaming response

def main(path=None):

    # Configure basic logging
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    # Configure more logging, if found
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as stream:
            dictConfig(yaml.safe_load(stream))

    # Create the server
    server = web.Application()
    server.on_startup.append(initialize)

    # Add the routes
    # server.add_routes([web.get('/', index, name='index'),
    #                    web.post('/', dispatch)])


    static_files = Path(__file__).parent.parent / 'static'
    server.add_routes([web.get('/', index, name='index'),
                       web.post('/', dispatch),
                       web.static('/static', str(static_files))])

    # .... and cue music!
    LOG.info(f"Start services registry UI")
    # .... and cue music
    if path:
        if os.path.exists(path):
            os.unlink(path)
        # will create the UDS socket and bind to it
        web.run_app(server,
                    path=path,
                    shutdown_timeout=0,
                    ssl_context=getattr(conf, 'ui_ssl_context', None))
    else:
        web.run_app(server,
                    host=getattr(conf, 'ui_host', '0.0.0.0'),
                    port=getattr(conf, 'ui_port', 8001),
                    shutdown_timeout=0,
                    ssl_context=getattr(conf, 'ssl_context', None))


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1: # Unix socket
        main(path=sys.argv[1])
    else: # host:port
        main()
