
from .. import conf

def ga4gh_service_info_v10(row):
    return {
        'id': conf.service_info['id'],
        'name': conf.service_info['name'],
        'type': {
            'group': conf.ga4gh_service_info_group,
            'artifact': conf.ga4gh_service_info_artifact,
            'version': conf.api_version
        },
        'description': conf.service_info['description'],
        'organization': {
            'name': conf.service_info['organization']['name'],
            'url': conf.service_info['organization']['welcomeUrl'],
        },
        'contactUrl': None,
        'documentationUrl': None,
        'createdAt': conf.service_info['createDateTime'],
        'updatedAt': conf.service_info['updateDateTime'],
        'environment': None,
        'version': conf.service_info['version'],
    }