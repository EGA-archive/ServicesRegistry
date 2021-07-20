import logging
from aiohttp import web
import httpx
import json

from .. import conf
from ..validation import path_validator
from ..utils import Collector

LOG = logging.getLogger(__name__)

collector = Collector(conf.services)

async def forward(request):
    LOG.info('-------- Aggregator query %s', request.path_qs)

    # Validate the path, raise error if fail
    await path_validator.validate(request)

    # Collect the responses
    path = request.match_info.get('anything', request.path_qs)

    #json = (request.headers.get('Accept','').lower() == 'application/json')
    json = True

    data = None
    if request.method == 'POST':
        data = await request.post() # Not json(), no need to parse+serialize

    results = await collector.request(request.method,
                                      path,
                                      headers=request.headers,
                                      data=data,
                                      json=json)
    responses = {}
    for (name, url, response, error) in results:
        if response: # and not error
            responses[name] = {'request': request.method + ' ' + url, 'response': response }
        else:
            responses[name] = {'request': request.method + ' ' + url, 'error': error }

    LOG.info('-------- Aggregator query %s | responses %d', request.path_qs, len(responses))
    # d = json.dumps(responses)
    # LOG.info('-------- sending %s', d)
    # return web.Response(text=d, content_type='application/json')
    return web.json_response(responses)  # change that for streaming response
