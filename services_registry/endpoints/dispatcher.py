import logging
from aiohttp import web
import httpx

from services_registry import conf
from ..validation import path_validator
from ..utils import collect_responses

LOG = logging.getLogger(__name__)


# @routes.get('/{anything:.+}')
async def forward_endpoint(request):
    LOG.info('-------- Aggregator query %s', request.path_qs)

    # Validate the path, raise error if fail
    await path_validator.validate(request)

    # Collect the responses
    data = request.post() if request.method == 'POST' else None
    results = await collect_responses(request.path_qs,
                                      method=request.method,
                                      headers=request.headers,
                                      data=data,
                                      json=True)
    responses = [(name, {'request': url, 'response': response})
                 for (name, url, response, error) in results]

    res = dict(responses)
    LOG.debug('==================')
    LOG.debug('responses: %s', res)
    return web.json_response(res)  # change that for streaming response


# async def _get_responses_from_path(path):
#     LOG.debug('get_responses_from_path(%s)', path)

#     if path is None:
#         raise web.HTTPInternalServerError(reason='path cannot be empty')

#     results = await collect_responses(path)
#     responses = [(name, {'request': url, 'response': response})
#                  for (name, url, response, error) in results]
    
#     return dict(responses)

# async def forward_specific_path(path):
#     LOG.info('-------- Aggregator query %s', path)

#     # await validator.validate(request) # it will raise an error if path is not valid

#     response = await _get_responses_from_path(path=path)
#     return web.json_response(dict([r async for r in response]))  # change that for streaming response
