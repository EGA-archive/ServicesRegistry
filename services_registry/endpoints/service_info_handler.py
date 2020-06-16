import logging
from aiohttp import web

from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import Field, ChoiceField, SchemasField
from ..response.response import json_stream
from ..response.response_schema import build_service_response, build_service_info_response
from ..schemas import default, alternative, SUPPORTED_SCHEMAS
from .. import conf

LOG = logging.getLogger(__name__)

routes = web.RouteTableDef()


# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class ServiceInfoParameters(RequestParameters):
    serviceType = ChoiceField(i for i in conf.service_types)
    model = SchemasField()
    listFormat = ChoiceField('short', 'full', default='full')
    apiVersion = Field(default=None)
    requestedSchemasServiceInfo = SchemasField()

    def correlate(self, req, values):
        LOG.info('Further correlation for the services endpoint')
        if values.apiVersion is not None and values.model is None:
            raise web.HTTPBadRequest(reason="Parameter 'model' is required when using 'apiVersion'")

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

    if qparams_db.model is not None:
        return await handler_service_info(request)

    response_converted = build_service_response(None, qparams_db, build_service_info_response)
    return await json_stream(request, response_converted)


@routes.get('/service-info')
async def handler_service_info(request):
    LOG.info('Running a GET service-info request')

    return await json_stream(request, alternative.ga4gh_service_info_v10(None))