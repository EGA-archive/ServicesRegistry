import logging
from aiohttp import web

from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import Field, ChoiceField, SchemasField
from ..response.response import json_stream
from ..response.response_schema import build_service_response, build_service_info_response
from .. import conf
from ..utils import Collector


LOG = logging.getLogger(__name__)

_keys = ('name', 'url', 'response', 'error')

async def handler(request):
    LOG.info('Running a GET cohorts request')

    collector = Collector(conf.services)
    cohorts = await collector.get('/cohorts') # it will prepend /api
    datasets = await collector.get('/datasets')

    LOG.debug('cohorts: %s', cohorts)
    LOG.debug('datasets: %s', datasets)

    response = {
        'cohorts': [dict(zip(_keys, res)) for res in cohorts],
        'datasets': [dict(zip(_keys, res)) for res in datasets],
    }
    return await json_stream(request, response)

