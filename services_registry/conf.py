host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = {
	'eu.crg.covid19beacon': {
		'name': 'Covid Beacon',
		'address': 'https://covid19beacon.crg.eu/api/'
	},
	'ca.distributedgenomics.poc': {
		'name': 'CANDIG',
		'address': 'https://poc.distributedgenomics.ca:5050'
	}
}

urls_whitelisted = [r'^/$',
					r'^/query?.*',
					r'^/g_variants.*',
					r'^/biosamples.*',
					r'^/datasets',
					r'^/cohorts']

urls_blacklisted = []

service_id = 'eu.crg.services-registry'
service_name = 'Service Registry'
service_version = '2.0'
api_version = 'v2.0.0-draft.1'

ga4gh_service_info_group = 'org.ga4gh'
ga4gh_service_info_artifact = 'service-registry'
ga4gh_version = '1.0'
ga4gh_service_types = ['org.ga4gh.service-registry.1.0', 'org.ga4gh.beacon-aggregator.1.0', 'org.ga4gh.beacon.1.0']