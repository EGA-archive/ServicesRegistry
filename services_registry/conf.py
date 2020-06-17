host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = [ #('EGA Beacon v0.3', 'https://ega-archive.org/beacon-api/'),
			#('EGA Beacon', 'https://beacon-api.ega-archive.org'),
			 ('Covid Beacon', 'https://covid19beacon.crg.eu/api/'),
			 ('CANDIG', 'https://poc.distributedgenomics.ca:5050')]


urls_whitelisted = [r'^/$',
					r'^/service-info$',
					r'^/services$',
					r'^/query?.*',
					r'^/g_variants.*',
					r'^/biosamples.*',]

urls_blacklisted = []

service_id = 'eu.crg.services-registry'
service_name = ''
service_version = '2.0'
api_version = 'v2.0.0-draft.1'

ga4gh_service_info_group = 'org.ga4gh'
ga4gh_service_info_artifact = 'service-registry'
ga4gh_version = '1.0'
ga4gh_service_types = ['org.ga4gh.service-registry.1.0', 'org.ga4gh.beacon-aggregator.1.0', 'org.ga4gh.beacon.1.0']