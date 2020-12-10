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

from .utils import Collector

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


def explore_service(name, url, info, error):
    """Fetch the interesting information of a service
    by using its base URL"""

    # LOG.info("Exploring %s: %s", name, url)
    # LOG.info("==> [error: %s] %s", error, info)

    # import pprint
    # pprint.pprint(info)

    if error:
        return {
            "title": name,
            "error": error,
            "url": url
        }

    try:
        info = info['response']['results']
        org = info.get("organization") or {}
        return {
            "title": name,
            "error": error,
            "organization_name": org.get("name"),
            "name": info.get("name"),
            "description": info.get("description"),
            "visit_us": org.get("welcomeUrl"),
            "beacon_api": info.get("welcomeUrl"),
            "contact_us": org.get("contactUrl"),
            "logo_url": org.get("logoUrl", ''),
        }
    except KeyError as e:
        return {
            "title": name,
            "error": str(e),
            "url": url
        }
        

@aiohttp_jinja2.template('index.html')
async def index(request):
    results = await collector.get('', json=True)
    services_info = [explore_service(*args) for args in results]
    return { "services": services_info }

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
