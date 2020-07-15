import logging
import asyncio
import time

import httpx

from .. import conf

TIMEOUT = getattr(conf, 'timeout', None)

LOG = logging.getLogger(__name__)

def now():
    return time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())

class Collector():
    
    def __init__(self, services, expire=None):
        self.expire_after = expire
        # Dict with service id mapping to a dict with {'name', 'address' }
        LOG.debug('---------------- Services: %s', services)
        self.services = services
        # Landing place for the calls: Dict with service id mapping to a dict with {'response', 'error' }
        self.cache = {}
        # mapping of service id to ('last_call_at', response or None, error)

    async def get(self, url, headers=None, json=True):
        """Return an iterator of (name, url, response, error)."""

        aws = [self._get_one(service_id,
                             d['name'],
                             d['address'].rstrip('/') + '/' + url.lstrip('/'),
                             dict(headers) if headers else None, # copy, and make it usable for each client
                             json)
               for service_id, d in self.services.items()]
        return [(await coro) for coro in asyncio.as_completed(aws)]

    async def _get_one(self, service_id, name, url, headers, json):
        LOG.info('CONTACT %s %s', name, url)
        try:
            # Check the cache
            last_call_at, response, error = self.cache.get(service_id, (None, None, None))
            if not error and response is not None and last_call_at is not None:
                # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.25
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Modified-Since
                # https://www.logicbig.com/quick-info/web/last-modified-and-if-modified-since.html
                headers = headers or {}
                headers['if-modified-since'] = last_call_at
                LOG.debug('---- Sending headers with if-modified-since: %s', last_call_at)
                            
            # Do the call
            #LOG.debug('---- GET %s | headers: %s', url, headers)
            async with httpx.AsyncClient() as client:
                r = await client.get(url, headers=headers)
                if r.status_code == 304:
                    last_call_at = r.headers.get('Last-Modified') or now()
                    error = None # and keep the response from the cache
                elif r.status_code == 200:
                    response = r.json() if json else r.content
                    error = None
                else: # error
                    raise ValueError(f'Error {r.status_code}')
        
                last_call_at = r.headers.get('Last-Modified') or now()
                # Save to cache
                self.cache[service_id] = (last_call_at, response, error)
                return (name, url, response, error)

        except Exception as e:
            LOG.error("Invalid response for %s: %s", name, e)
            return (name, url, None, str(e))


    async def post(self, url, headers=None, data=None, json=True):
        """Return an iterator of (name, url, response, error)."""

        async with httpx.AsyncClient() as client:
            aws = [self._post_one(client,
                                  d['name'],
                                  d['address'].rstrip('/') + '/' + url.lstrip('/'),
                                  headers,
                                  data,
                                  json)
                   for d in self.services.values()]
            return [(await coro) for coro in asyncio.as_completed(aws)]

    async def _post_one(self, client, name, url, headers, data, json):
        LOG.info('POST %s %s | headers: %s | data: %s', name, url, headers, data)
        try:
            r = await client.post(url, headers=headers, data=data, timeout=TIMEOUT)
            response = r.json() if json else r.content
            return (name, url, response, None)
        except Exception as e:
            LOG.error("Invalid response for %s: %s", name, e)
            return (name, url, None, str(e))
