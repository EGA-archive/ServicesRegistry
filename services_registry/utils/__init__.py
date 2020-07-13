import logging
import asyncio

import httpx

from ..conf import services

LOG = logging.getLogger(__name__)

async def get(name, url, headers, json=True, old):
    LOG.info('CONTACT %s %s', name, url)
    try:
        async with httpx.AsyncClient() as client:
            if old:
                headers_for_head = headers.clone() if headers else {}
                headers_for_head['if-modified-since'] = old['last_call_at']
                LOG.info('---- HEAD %s | headers: %s', url, headers_for_head)
                r = await client.head(url, headers=headers_for_head)
                if r.status_code == 304:
                    return old['response']

            LOG.info('---- GET %s | headers: %s', url, headers)
            r = await client.get(url) # no header
            response = r.json() if json else r.content
            error = False
    except Exception as e:
        LOG.error("Invalid response for %s: %s", name, e)
        response = str(e)
        error = True

    return (name, url, response, error)


async def collect_responses(url, method='GET', headers=None, data=None, json=True, services_list=None):
    """Return an iterator of (name, url, response, error)."""

    if services_list is None:
        services_list = services

    if not url or url[0] != '/':
        url = '/' + url
    aws = [get(d['name'], d['address'] + url, method, headers, data, json=json)
           for d in services_list.values()]
    return [await coro for coro in asyncio.as_completed(aws)]

class Collector():
    
    def __init__(self, expire):
        self.expire_after = expire

    async def collect(self, url):
        

    

def resolve_into(d):

    def decorator(func):

        async def wrapper(d, *args, **kwargs):
            d['response'] = await func(*args, **kwargs)
        return wrapper
    return decorator

            
