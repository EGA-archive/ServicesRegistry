import logging
from aiohttp import web
import httpx

from .dispatcher import forward_endpoint, forward_specific_path
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import Field, ChoiceField, SchemasField
from ..response.response import json_stream
from ..response.response_schema import build_service_response, build_service_info_response
from ..schemas import default, alternative, SUPPORTED_SCHEMAS
from .. import conf


LOG = logging.getLogger(__name__)

routes = web.RouteTableDef()

SERVICES = conf.services


# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class ServicesParameters(RequestParameters):
    serviceType = ChoiceField(i for i in conf.ga4gh_service_types) # TODO
    model = SchemasField()
    listFormat = ChoiceField('short', 'full', default='full') # TODO
    apiVersion = Field(default=None) # TODO
    requestedSchemasServiceInfo = SchemasField()

    def correlate(self, req, values):
        LOG.info('Further correlation for the services endpoint')
        if values.apiVersion is not None and values.model is None:
            raise web.HTTPBadRequest(reason="Parameter 'model' is required when using 'apiVersion'")

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

services_proxy = ServicesParameters()

@routes.get('/bn_services')
async def handler_services(request):
    LOG.info('Running a GET bn_services request')

    _, qparams_db = await services_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, services_proxy, LOG)

    if len(qparams_db.model[0]) > 0:
        response = response_from_services(path='/service-info')
        return web.json_response(list([r async for r in response]))

    # return await forward_specific_path('/info') # just concatenate responses
    return await forward_and_process_response(request, qparams_db, '/info')


@routes.get('/services')
async def handler_services(request):
    LOG.info('Running a GET GA4GH services request')

    response = response_from_services(path='/service-info')
    return web.json_response(list([r async for r in response]))


async def forward_and_process_response(request, qparams_db, path):
    LOG.info('-------- Aggregator query %s', path)

    # TODO forward the alternativeSchemas requested too?

    response = response_from_services(path=path)
    response_converted = build_service_response(list([r async for r in response]), qparams_db, build_service_info_response)
    return await json_stream(request, response_converted)


async def response_from_services(path, method='GET', post_data=None):
    LOG.info('-------- response_from_services %s', path)

    # Allow only GET and POST ?
    for name, address in SERVICES:
        url = f'{address}{path}'
        LOG.info('%s %s', method, url)
        async with httpx.AsyncClient() as client:
            r = await client.request(method,
                                     url,
                                     # headers=request.headers,
                                     data=None if method == 'GET' else post_data)
            if r.status_code > 200:
                LOG.error("Invalid response [%s] for %s", r.status_code, name)
                response = f"Invalid response {r.status_code}"
            else:
                response = r.json()

            yield response