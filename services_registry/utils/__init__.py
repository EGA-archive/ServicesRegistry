import httpx

# Create a type, as a str, which allow the JSON streamer
# to use it as it is and not escape the quotes
# Useful when we already have the JSON as a properly formatted string
# so we don't need to parse it and re-serialize it
class json_blob(str):
    pass


async def _fetch(name, url, method, headers, data):
    LOG.info('%s %s', method, url)
    async with httpx.AsyncClient() as client:
        r = await client.request(method,
                                 url,
                                 headers=headers,
                                 data=data)
        if r.status_code > 200:
            LOG.error("Invalid response [%s] for %s", r.status_code, name)
            response = f"Invalid response {r.status_code}"
        else:
            response = json_blob(await r.json())
        LOG.debug('Got result for %s', name)
        return (name, {'request': url, 'response': response})

async def iter_fetch(request):
    LOG.info('-------- iter_fetch %s', request.path_qs if request is not None else path)

    if request is None and path is None:
        raise web.HTTPInternalServerError(reason='Both request and path cannot be empty')

    method = 'GET'
    post_data = None
    if request is not None:
        path = request.path_qs
        method = request.method
        post_data = await request.post()

    # Allow only GET and POST ?
    for key, name, url in conf.services:
        url = f"{url}{path}"
        LOG.info('%s %s', method, url)
        _fetch(name, url, method, None, data):

        async with httpx.AsyncClient() as client:
            r = await client.request(method,
                                     url,
                                     # headers=request.headers,
                                     data=None if method == 'GET' else post_data)
            if r.status_code > 200:
                LOG.error("Invalid response [%s] for %s", r.status_code, name)
                response = f"Invalid response {r.status_code}"
            else:
                response = await r.json()

            yield (name, {'request': url, 'response': response})





async def _fetch(name, url, method, headers, data):
    async with httpx.AsyncClient() as client:
        r = await client.request(method,
                                 url,
                                 headers=headers,
                                 data=data)
        print(r)
        # if r.status_code > 200:
        #     LOG.error("Invalid response [%s] for %s", r.status_code, name)
        #     response = f"Invalid response {r.status_code}"
        # else:
        #     response = json_blob(await r.json())
        # LOG.debug('Got result for %s', name)
        # return (name, {'request': url, 'response': response})


async def collect(path):
    for key, name, url in conf.services:

aws = [_fetch(name, url, 'GET', None, None)
       for key, name, url in services]


async def run():
    result = {}
    for coro in asyncio.as_completed(aws):
        name, res = await coro
        result[name] = res
    print(result)
