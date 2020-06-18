import logging
from aiohttp import web

from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import ChoiceField, SchemasField
from ..response.response import json_stream
from ..response.response_schema import build_service_response, build_service_info_response, build_service_type_response
from ..schemas import alternative
from .. import conf

LOG = logging.getLogger(__name__)

routes = web.RouteTableDef()


# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class ServiceInfoParameters(RequestParameters):
    model = ChoiceField('ga4gh-service-info-v1.0', default=None)
    requestedSchemasServiceInfo = SchemasField()


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

service_info_proxy = ServiceInfoParameters()


# TODO add /
@routes.get('/info')
async def handler_info(request):
    LOG.info('Running a GET info request')
    _, qparams_db = await service_info_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, service_info_proxy, LOG)

    LOG.debug('model %s', qparams_db.model)
    if qparams_db.model is not None:
        return await handler_ga4gh_service_info(request)

    response_converted = build_service_response(None, qparams_db, build_service_info_response)
    return await json_stream(request, response_converted)


@routes.get('/service-info')
async def handler_ga4gh_service_info(request):
    LOG.info('Running a GET service-info request')

    return await json_stream(request, alternative.ga4gh_service_info_v10(None))


# Custom endpoint
@routes.get('/registered_services')
async def handler_registered_services(request):
    LOG.info('Running a GET registered services request')

    return await json_stream(request, conf.services)


@routes.get('/services/types')
async def handler_ga4gh_services_types(request):
    LOG.info('Running a GET GA4GH services types request')

    return await json_stream(request, conf.ga4gh_service_types)


@routes.get('/bn_service_types')
async def handler_services_types(request):
    LOG.info('Running a GET services types request')

    return await json_stream(request, conf.service_types)
