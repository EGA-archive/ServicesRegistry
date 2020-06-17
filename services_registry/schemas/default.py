
from .. import conf

def service_info_v01(row):
    if row is None:
        return {
            'id': conf.service_id,
            'name': conf.service_name,
            'serviceType': conf.ga4gh_service_info_group + '.' + conf.ga4gh_service_info_artifact,
            'apiVersion': conf.api_version,
            'serviceUrl': 'https://services-registry.crg.eu/api', # API
            'entryPoint': False,
            'organization': {
                'id': 'eu.crg',
                'name': 'Centre for Genomic Regulation (CRG)',
                'description': 'CRG is an international biomedical research institute of excellence, created in December 2000. It is a non-profit foundation funded by the Catalan Government through the Departments of Business & Knowledge, the Spanish Ministry of Science, Innovation & Universities, the \"la Caixa\" Banking Foundation, and includes the participation of Pompeu Fabra University',
                'address': 'Centre for Genomic Regulation (CRG) C/ Dr. Aiguader, 88. PRBB Building. 08003 Barcelona, Spain. Tel. +34 93 316 01 00 Fax +34 93 316 00 99',
                'welcomeUrl': 'https://www.crg.eu',
                'contactUrl': 'mailto:communications@crg.eu',
                'logoUrl': '/static/img/crg.png',
                'info': None
            },
            'description': 'This is a registry for services of any kind.',
            'version': conf.service_version,
            'open': True,
            'welcomeUrl': 'https://services-registry.crg.eu', # UI
            'alternativeUrl': None,
            'createDateTime': None,
            'updateDateTime': None
        }
    else:
        return row # just return it as it is