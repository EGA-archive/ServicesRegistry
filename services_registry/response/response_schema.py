import logging

from .. import conf
from ..schemas import SUPPORTED_SCHEMAS, DEFAULT_SCHEMAS

LOG = logging.getLogger(__name__)


def build_service_response(data, qparams_converted, func_response_type):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams_converted, func_response_type),
        'response': build_response(data, qparams_converted, func_response_type)
    }
    return beacon_response


def build_meta(qparams, func_response_type):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """

    meta = {
        'serviceId' : conf.service_id,
        'apiVersion': conf.api_version,
        'receivedRequest' : build_received_request(qparams),
        'returnedSchemas': build_returned_schemas(qparams, func_response_type)
    }
    return meta


def build_received_request(qparams):
    """"Fills the `receivedRequest` part with the request data"""

    request = {
        'meta': {
            'requestedSchemas' : build_requested_schemas(qparams),
            'apiVersion' : None,
        },
        'query': None
    }
    return request


def build_requested_schemas(qparams):
    """"
    Fills the `requestedSchemas` part with the request data
    It includes valid and invalid schemas requested by the user.
    """

    requested_schemas = {}

    # TODO
    if qparams.requestedSchemasServiceInfo[0] or qparams.requestedSchemasServiceInfo[1]:
        requested_schemas['ServiceInfo'] = [s for s, f in qparams.requestedSchemasServiceInfo[0]] + list(
            qparams.requestedSchemasServiceInfo[1])

    return requested_schemas


def build_returned_schemas(qparams, func_response_type):
    """"
    Fills the `returnedSchema` part with the actual schemas returned in the response.
    This is the default schema for each type and any valid schema requested by the user.
    """

    # LOG.debug('func_response_type= %s', func_response_type.__name__)

    returned_schemas_by_response_type = {
        'build_service_info_response': {
            'ServiceInfo': [DEFAULT_SCHEMAS['ServiceInfo']] + [s for s, f in qparams.requestedSchemasServiceInfo[0]],
        },
        'build_service_type_response': {
            'ServiceType': [DEFAULT_SCHEMAS['ServiceType']] # No other schemas available
        },
    }

    return returned_schemas_by_response_type[func_response_type.__name__] # We let it throw a KeyError


def build_error(qparams):
    """"
    Fills the `error` part in the response.
    This error only applies to partial errors which do not prevent the Beacon from answering.
    """

    if not qparams.requestedSchemasServiceInfo[1]:
         # Do nothing
         return

    message = 'Some requested schemas are not supported.'

    if len(qparams.requestedSchemasServiceInfo[1]) > 0:
        message += f' ServiceInfo: {qparams.requestedSchemasServiceInfo[1]}'


    return {
        'error': {
            'errorCode': 206,
            'errorMessage': message
        }
    }


def build_response(data, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""


    response = {
            'exists': True if data is None or len(data) > 0 else False,
            'results': func(data, qparams),
            'info': None,
            'resultsHandover': None, # build_results_handover
            'beaconHandover': None, # build_beacon_handover
        }

    error = build_error(qparams)
    if error is not None:
        response['error'] = error

    return response


def build_service_info_response(data, qparams):
    """"Fills the `results` part with the format for ServiceInfo"""

    service_info_requested_schemas = qparams.requestedSchemasServiceInfo[0]

    if data is None:
        LOG.debug('data is None')
        yield transform_data_into_schema(None, 'ServiceInfo', service_info_requested_schemas)
    else:
        LOG.debug('data is NOT None')
        for row in data:
            yield transform_data_into_schema(row, 'ServiceInfo', service_info_requested_schemas)


def build_service_type_response(data, qparams):
    """"Fills the `results` part with the format for ServiceType"""

    yield transform_data_into_schema(None, 'ServiceType', None)


def transform_data_into_schema(row, field_name, requested_schemas):
    """"Fills the content with the 2 types of schemas"""

    return {
        'defaultSchema': next(find_schemas(row, field_name)),
        'alternativeSchemas': find_schemas(row, field_name, (requested_schemas or []))
    }


def find_schemas(row, field_name, schemas=None):
    """"Returns the data transformed into the specified schema(s)"""
    LOG.debug('schemas: %s', schemas)

    if schemas is None:
        default_schema = DEFAULT_SCHEMAS[field_name] # We let it throw a KeyError
        schemas = [(default_schema, SUPPORTED_SCHEMAS[default_schema])]

    for schema, func in schemas:
        LOG.debug(f'schema: {schema}, func: {func}')
        yield {
            'version': schema,
            'value': func(row)
        }

