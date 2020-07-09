import datetime

from .. import conf

def service_info_v01(row):
    if row is None:
        return {
            'id': conf.service_id,
            'name': conf.service_name,
            'serviceType': conf.elixir_service_type_group + '.' + conf.elixir_service_type_artifact,
            'apiVersion': conf.api_version,
            'serviceUrl': 'https://cineca-services-registry.ega-archive.org/api', # API
            'entryPoint': False,
            'organization': {
                'id': 'eu.crg',
                'name': 'Centre for Genomic Regulation (CRG)',
                'description': 'CRG is an international biomedical research institute of excellence, created in December 2000. It is a non-profit foundation funded by the Catalan Government through the Departments of Business & Knowledge, the Spanish Ministry of Science, Innovation & Universities, the \"la Caixa\" Banking Foundation, and includes the participation of Pompeu Fabra University',
                'address': 'Centre for Genomic Regulation (CRG) C/ Dr. Aiguader, 88. PRBB Building. 08003 Barcelona, Spain. Tel. +34 93 316 01 00 Fax +34 93 316 00 99',
                'welcomeUrl': 'https://www.crg.eu',
                'contactUrl': 'mailto:beacon.ega@crg.eu',
                'logoUrl': 'https://www.crg.eu/sites/default/files/logo_1.png',
                'info': None
            },
            'description': 'This is a registry for services of any kind.',
            'version': conf.service_version,
            'open': True,
            'welcomeUrl': 'https://cineca-services-registry.ega-archive.org', # UI
            'alternativeUrl': None,
            'createDateTime': '2020-06-18T18:00.000Z',
            'updateDateTime': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    else:
        return row # just return it as it is
