import logging

from .. import conf
from .default import service_info_v01

LOG = logging.getLogger(__name__)


# noinspection PyDictCreation
def ga4gh_service_info_v10(row):

    group = None
    artifact = None
    version = None
    url = None

    if row is None:
        # Data for this registry
        row = service_info_v01(None)
        group = conf.ga4gh_service_type_group
        artifact = conf.ga4gh_service_type_artifact
        version = conf.ga4gh_service_type_version
    else:
        # Data for other services registered

        call_get = getattr(row, "get", None)
        if not callable(call_get):
            # e.g. the service is returning an error
            return row

        url = row.get('url')
        version = row.get('apiVersion')
        service_type = row.get('serviceType', None)
        if service_type is not None:
            tokens = service_type.rsplit('.', 1)
            if len(tokens) > 1:
                group = tokens[0]
                artifact = tokens[1]

    schema = {
        'id': row['id'],
        'name': row['name'],
        'type': {
            'group': group,
            'artifact': artifact,
            'version': version # TODO get this from the /info endpoint
        },
        'description': row['description'],
        'organization': {
            'name': row['organization']['name'],
            'url': row['organization']['welcomeUrl'],
        },
        'contactUrl': None,
        'documentationUrl': None,
        'createdAt': row['createDateTime'],
        'updatedAt': row['updateDateTime'],
        'environment': None,
        'version': row['version'],
    }

    if url is not None:
        schema['url'] = url

    return schema
