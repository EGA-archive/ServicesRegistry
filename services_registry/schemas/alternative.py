import logging

from .. import conf
from .default import service_info_v01

LOG = logging.getLogger(__name__)


def ga4gh_service_info_v10(row):

    group = None
    artifact = None
    version = None

    if row is None:
        # Data for this registry
        row = service_info_v01(None)
        group = conf.ga4gh_service_info_group
        artifact = conf.ga4gh_service_info_artifact
        version = conf.ga4gh_version
    else:
        # Data for other services registered
        service_type = row.get('serviceType', None)
        if service_type is not None:
            tokens = service_type.rsplit('.', 1)
            if len(tokens) > 1:
                group = tokens[0]
                artifact = tokens[1]

    return {
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
