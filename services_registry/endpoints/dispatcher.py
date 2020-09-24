import logging
from aiohttp import web
import httpx

from .. import conf
from ..validation import path_validator
from ..utils import Collector

LOG = logging.getLogger(__name__)

collector = Collector(conf.services)

async def forward_get(request):
    LOG.info('-------- Aggregator query %s', request.path_qs)

    # Validate the path, raise error if fail
    await path_validator.validate(request)

    # Collect the responses
    path = request.match_info.get('anything', request.path_qs)
    results = await collector.get(path,
                                  headers=request.headers,
                                  json=True)
    responses = {}
    for (name, url, response, error) in results:
        if response: # and not error
            responses[name] = {'request': url, 'response': response }
        else:
            responses[name] = {'request': url, 'error': error }

    return web.json_response(responses)  # change that for streaming response

async def forward_post(request):
    LOG.info('-------- Aggregator query %s', request.path_qs)

    # Validate the path, raise error if fail
    await path_validator.validate(request)

    # Collect the responses
    path = request.match_info.get('anything', request.path_qs)
    results = await collector.post(request.path_qs,
                                   headers=request.headers,
                                   data=request.post(), # Not json(), no need to parse+serialize
                                   json=True)
    responses = {}
    for (name, url, response, error) in results:
        if response: # and not error
            responses[name] = {'request': url, 'response': response }
        else:
            responses[name] = {'request': url, 'error': error }

    return web.json_response(responses)  # change that for streaming response
