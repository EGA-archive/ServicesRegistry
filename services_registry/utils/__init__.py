import logging
import asyncio

import httpx

from ..conf import services

LOG = logging.getLogger(__name__)

async def fetch(name, url, method, headers, data, json=True):
    LOG.info('%s %s', method, url)
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url) # no header
            LOG.info('---- [%s] %s: %s', name, url, r)
            response = r.json() if json else r.content
            error = False
    except Exception as e:
        LOG.error("Invalid response for %s: %s", name, e)
        response = str(e)
        error = True

    return (name, url, response, error)


async def collect_responses(url, method='GET', headers=None, data=None, json=True):
    '''Return an iterator of (name, url, response, error).'''
    if not url or url[0] != '/':
        url = '/' + url
    aws = [fetch(d['name'], d['address'] + url, method, headers, data, json=json)
           for d in services.values()]
    return [await coro for coro in asyncio.as_completed(aws)]


