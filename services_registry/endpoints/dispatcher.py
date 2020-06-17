import logging
from aiohttp import web
import httpx

from services_registry import conf
from ..validator import validator

LOG = logging.getLogger(__name__)

routes = web.RouteTableDef()

SERVICES = conf.services

async def response_from_services(request=None, path=None):
    LOG.info('-------- response_from_services %s', request.path_qs if request is not None else path)

    if request is None and path is None:
        raise web.HTTPInternalServerError(reason='Both request and path cannot be empty')

    method = 'GET'
    post_data = None
    if request is not None:
        path = request.path_qs
        method = request.method
        post_data = request.post()

    # Allow only GET and POST ?
    for key, service in SERVICES.items():
        url = f"{service['address']}{path}"
        LOG.info('%s %s', method, url)
        async with httpx.AsyncClient() as client:
            r = await client.request(method,
                                     url,
                                     # headers=request.headers,
                                     data=None if method == 'GET' else post_data)
            if r.status_code > 200:
                LOG.error("Invalid response [%s] for %s", r.status_code, service['name'])
                response = f"Invalid response {r.status_code}"
            else:
                response = r.json()

            yield (service['name'], {'request': url, 'response': response})


@routes.get('/{anything:.*}')
async def forward_endpoint(request):
    LOG.info('-------- Aggregator query %s', request.path_qs)

    await validator.validate(request) # it will raise an error if path is not valid

    response = response_from_services(request)
    return web.json_response(dict([r async for r in response]))  # change that for streaming response


async def forward_specific_path(path):
    LOG.info('-------- Aggregator query %s', path)

    # await validator.validate(request) # it will raise an error if path is not valid

    response = response_from_services(path=path)
    return web.json_response(dict([r async for r in response]))  # change that for streaming response