"""Service Registry"""

import sys
import os
import logging
from logging.config import dictConfig
from pathlib import Path
import asyncio
from urllib.parse import quote
import json
from datetime import datetime
from humanize import naturaltime

import yaml
from aiohttp import web
import aiohttp_jinja2
import jinja2
import httpx


from . import conf

from .utils import Collector
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

def check_url_exist(url):
    if not url:
        return None
    try:
        r = httpx.get(url)
        if r.status_code != 200:
            return None
    except Exception as e:
        LOG.error('Error: %s', e)
    return url

def check_logo(url):
    if not url:
        return getattr(conf, 'default_logo', '/static/img/no_logo.png')
    r = httpx.get(url)
    if r.status_code != 200:
        return getattr(conf, 'default_logo', '/static/img/no_logo.png')
    return url

def valid_filter(dic, valid_type):
    return dic['valid'] is valid_type

def explore_service(name, url, order, verifier, info, error):
    """Fetch the interesting information of a service
    by using its base URL"""

    if error:
        return {
            "title": name,
            "error": error,
            "url": url
        }

    response = info.get('response', {})
    results = response.get('results')
    if results:
        response = results # Supporting the old format
    org = response.get("organization", {})
    beacon_id = response.get('id') or response.get('beaconId')
    entities_json_file = f'static/entities/{verifier}';
    d = {
        "beaconId": beacon_id,
        "title": name,
        "organization_name": org.get("name"),
        "name": response.get("name"),
        "description": response.get("description"),
        "visit_us": check_url_exist(org.get("welcomeUrl")),
        "beacon_ui": check_url_exist(response.get("welcomeUrl")),
        "beacon_api": url,
        "contact_us": org.get("contactUrl"),
        "logo_exist": check_url_exist(org.get("logoUrl")),
        "logo_url": check_logo(org.get("logoUrl")),
        "order": order
    }
    try:
        with open(entities_json_file) as fh:
            entities = json.load(fh)
            now = datetime.now()
            last_updated = datetime.strptime(entities['last_updated'], '%Y-%m-%dT%H:%M:%S.%f')
            d["last_updated"] = naturaltime(now-last_updated)
            d["entities"] = entities['entities']
            d["entities_count"] = {}
            for group_name, entity in d["entities"].items():
                count_all = len(entity)
                count_valid = len([d for d in entity if valid_filter(d, True)])
                count_error = len([d for d in entity if valid_filter(d, False)])
                percentage_valid = (100*count_valid)/count_all
                percentage_error = (100*count_error)/count_all
                d["entities_count"][group_name] = {
                    'valid_percentage': percentage_valid,
                    'error_percentage': percentage_error
                }
    except Exception as e:
        LOG.error('Error on %s: %s', entities_json_file, e)
    return d

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
