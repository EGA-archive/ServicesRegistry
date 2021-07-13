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

    def clean_headers(self, headers):
        if not headers:
            return None
        return dict((k,v) for k,v in headers.items()
                    if k not in ('Host', 'Content-Length', 'Content-Type'))

    def clean_data(self, data):
        if not data:
            return None
        return dict((k,v) for k,v in data.items())


    async def request(self, method, url, headers=None, data=None, json=True):
        """Return an iterator of (name, url, response, error)."""

        headers = self.clean_headers(headers)
        data = self.clean_data(data)

        LOG.info('DISPATCHING %s %s', method, url)
        LOG.info('\t headers: %s', headers)
        LOG.info('\t data: %s', data)

        aws = [self._request_one(method,
                                 service_id,
                                 d['name'],
                                 #d['address'].rstrip('/') + '/' + url.lstrip('/'),
                                 d['address'].rstrip('/') + url,
                                 headers,
                                 data,
                                 json)
               for service_id, d in self.services.items()]
        return [(await coro) for coro in asyncio.as_completed(aws)]

    async def _request_one(self, method, service_id, name, url, headers, data, json):
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
            LOG.debug('---- %s %s | headers: %s', method, url, headers)
            async with httpx.AsyncClient() as client:
                r = await client.request(method, url, headers=headers, data=data)
                LOG.debug('---- status: %s', r.status_code)
                if r.status_code == 304:
                    last_call_at = r.headers.get('Last-Modified') or now()
                    error = None # and keep the response from the cache
                elif r.status_code == 200:
                    #LOG.info('response: %s', r.content[:50])
                    response = r.json() if json else r.content
                    error = None
                else: # error
                    raise ValueError(f'Error {r.status_code}: {r.content}')
        
                last_call_at = r.headers.get('Last-Modified') or now()
                # Save to cache
                self.cache[service_id] = (last_call_at, response, error)
                return (name, url, response, error)

        except httpx.TimeoutException as e:
            LOG.error("Connection Timeout %s: %r", name, e)
            return (name, url, None, "Service not available")
        except Exception as e:
            LOG.error("Invalid response for %s: %r", name, e)
            return (name, url, None, repr(e))
