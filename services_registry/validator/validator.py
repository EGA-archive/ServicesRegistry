import logging
import re
from aiohttp import web

from ..dispatcher import forward_endpoint
from .. import conf

LOG = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.view('/favicon.ico')
class Validator(web.View):

    async def get(self):
        raise web.HTTPNotFound()


@routes.view('/{anything:.*}')
class Validator(web.View):

    async def get(self):
        LOG.info('Validator - GET')

        path = self.request.path
        LOG.debug('Validating path: %s', path)

        if conf.urls_blacklisted and re.search(r"(?=("+'|'.join(conf.urls_blacklisted)+r"))", path):
            LOG.error('path in the blacklist: %s', path)
            raise web.HTTPForbidden()

        match = re.search(r"(?=("+'|'.join(conf.urls_whitelisted)+r"))", path)
        if match:
            LOG.debug('match %s', match.group(0))

        if conf.urls_whitelisted and not re.search(r"(?=("+'|'.join(conf.urls_whitelisted)+r"))", path):
            LOG.error('path not in the whitelist: %s', path)
            raise web.HTTPForbidden()

        # use self.request.query_string to d any validation on the query parameters

        return await forward_endpoint(self.request)

