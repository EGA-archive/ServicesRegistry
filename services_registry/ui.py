"""Service Registry"""

import sys
import os
import logging
from logging.config import dictConfig
from pathlib import Path
import yaml
import httpx

from aiohttp import web

from . import conf

LOG = logging.getLogger(__name__)
LOG_FILE = Path(os.getenv('SERVICES_REGISTRY_LOG', 'logger.yml')).resolve()


async def initialize(app):
    """Initialize HTTP server."""

    # Configure CORS settings
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    # Apply CORS to endpoints
    for route in list(app.router.routes()):
        cors.add(route)

    # Setup the HTML templates
    templates_path = Path(__file__).parent / 'templates'
    LOG.debug('template directory: %s', str(templates_path))
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(str(templates_path)))
    app['static_root_url'] = '/static'
    # env = aiohttp_jinja2.get_env(app)
    # env.globals.update(
    #     len=len,
    #     max=max,
    #     enumerate=enumerate,
    #     range=range)
    LOG.info("Initialization done.")


async def explore_service(name, service_url):
    """Fetch the interesting information of a service
    by using its base URL"""
    service = {}

    # Use the name and address keys of the service input dictionary
    service["title"] = name

    # Fetch the info page of the service
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(service_url) # no header
            service["error"] = False
            info = r.json()

            org = info["organization"]
            service["organization_name"] = org["name"]
            service["name"] = info["name"] # reset
            service["description"] = info["description"]
            service["visit_us"] = org["welcomeUrl"]
            service["beacon_api"] = info["welcomeUrl"]
            service["contact_us"] = org["contactUrl"]

            # For the logo, we need to check if the link is OK
            logo_url = info["organization"]["logoUrl"]
            service["logo_url"] = service_url + logo_url if not logo_url.startswith("http") else logo_url
    except Exception as e:
        service["error"] = True

    LOG.info('------ [%s] %s: %s', name, service_url, service)
    return service

@aiohttp_jinja2.template('index.html')
async def index(request):
    aws = [explore_service(d['name'], d['address'])
           for d in conf.services]
    services_info = [await coro
                     for coro in asyncio.as_completed(aws)]
    return { "services": services_info }


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
    server.add_routes([web.get('/', index, name='index')])

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
