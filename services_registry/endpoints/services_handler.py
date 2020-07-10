import logging
from aiohttp import web
import httpx

from .dispatcher import forward_endpoint
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import Field, ChoiceField, SchemasField
from ..response.response import json_stream
from ..response.response_schema import build_service_response, build_service_info_response
from ..schemas import default, alternative, SUPPORTED_SCHEMAS
from .. import conf
from ..utils import collect_responses


LOG = logging.getLogger(__name__)

SERVICES = conf.services


# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class ServicesParameters(RequestParameters):
    serviceType = ChoiceField(i for i in conf.service_types) # TODO
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


async def handler_services(request):
    LOG.info('Running a GET bn_services request')

    _, qparams_db = await services_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, services_proxy, LOG)

    if len(qparams_db.model[0]) > 0:
        response = await response_from_services(path='/service-info')
        return web.json_response(list([ resp for (name, url, resp, error) in response]))

    return await forward_and_process_response(request, qparams_db, '/info')


async def handler_services_by_id(request):
    LOG.info('Running a GET bn_services by ID request')

    _, qparams_db = await services_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, services_proxy, LOG)

    requested_service_id = request.match_info['service_id']

    if len(qparams_db.model[0]) > 0:
        response = await response_from_services(path='/service-info', requested_service_id=requested_service_id)
        return web.json_response(list([ resp for (name, url, resp, error) in response]))

    return await forward_and_process_response(request, qparams_db, '/info', requested_service_id=requested_service_id)


async def handler_ga4gh_services(request):
    LOG.info('Running a GET GA4GH services request')

    response = await response_from_services(path='/service-info')
    return web.json_response(list([ resp for (name, url, resp, error) in response]))


async def handler_ga4gh_services_by_id(request):
    LOG.info('Running a GET GA4GH services by ID request')

    requested_service_id = request.match_info['service_id']

    response = await response_from_services(path='/service-info', requested_service_id=requested_service_id)
    return web.json_response(list([ resp for (name, url, resp, error) in response]))


async def forward_and_process_response(request, qparams_db, path, requested_service_id=None):
    LOG.info('-------- Aggregator query %s', path)

    # TODO forward the alternativeSchemas requested too?

    response = await response_from_services(path=path, requested_service_id=requested_service_id)
    response_converted = build_service_response(list([ resp for (name, url, resp, error) in response]),
                                                qparams_db,
                                                build_service_info_response)
    return await json_stream(request, response_converted)


async def response_from_services(path, requested_service_id=None, method='GET', post_data=None):
    LOG.info('-------- response_from_services %s', path)

    return await collect_responses(path, services_list={
        requested_service_id: SERVICES[requested_service_id]
    } if requested_service_id is not None else SERVICES)
