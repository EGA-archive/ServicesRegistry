host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = [ ('EGA Beacon v0.3', 'https://ega-archive.org/beacon-api/'),
			#('EGA Beacon', 'https://beacon-api.ega-archive.org'),
			 ('Covid Beacon', 'https://covid19beacon.crg.eu/api/')]


urls_whitelisted = [r'^/$',
					r'^/service-info$',
					r'^/query?.*',
					r'^/g_variants.*',
					r'^/biosamples.*',]

urls_blacklisted = []

service_types = ['org.ga4gh.registry.0.1', 'org.ga4gh.beacon.1.0', 'org.ga4gh.beacon.2.0']

ga4gh_service_info_group = 'org.ga4gh'
ga4gh_service_info_artifact = 'registry'
version = '0.1'

service_info = {
	'id': 'eu.crg.services-registry',
	'name': 'Services Registry',
	'serviceType': ga4gh_service_info_group + '.' + ga4gh_service_info_artifact + '.' + version,
	'apiVersion': 'v2.0.0-draft.1',
	'serviceUrl': 'TODO',
	'entryPoint': False,
	'organization': {
		'id': 'eu.crg',
		'name': 'Centre for Genomic Regulation (CRG)',
		'description': None,
		'address': 'C/ Dr. Aiguader, 88. 08001 Barcelona (Spain)',
		'welcomeUrl': 'www.crg.eu',
		'contactUrl': None,
		'logoUrl': None,
		'info': None
	},
	'description': 'This is a registry for services of any kind.',
	'version': version,
	'open': True,
	'welcomeUrl': None,
	'alternativeUrl': None,
	'createDateTime': None,
	'updateDateTime': None
}