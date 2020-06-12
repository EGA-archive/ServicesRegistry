import logging
from aiohttp import web
import httpx

from . import conf

LOG = logging.getLogger(__name__)

SERVICES = conf.services

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

            yield (name, {'request': url, 'response': response})


async def forward_endpoint(request):
    LOG.info('-------- Aggregator query %s', request.path_qs)
    response = response_from_services(request)
    return web.json_response(dict([r async for r in response]))  # change that for streaming response