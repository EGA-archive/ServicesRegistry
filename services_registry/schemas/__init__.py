from . import default, alternative


SUPPORTED_SCHEMAS = {
    'elixirbn-service-info-v0.1': default.service_info_v01,
    'ga4gh-service-info-v1.0': alternative.ga4gh_service_info_v10,
}


DEFAULT_SCHEMAS = {
    'ServiceInfo': 'elixirbn-service-info-v0.1',
}


def partition(schemas):
    valid, invalid = set(), set() # avoid repetitions
    for schema in schemas:
        func = SUPPORTED_SCHEMAS.get(schema)
        if func is None:
            invalid.add(schema)
        else:
            valid.add((schema,func))
    return (valid, invalid)