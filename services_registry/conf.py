host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = {
	'ca.distributedgenomics.poc': {
		'name': 'PseudoCHILD Beacon',
		'address': 'https://poc.distributedgenomics.ca:5050'
	},
	'h3abionet-test-beacon': {
		'name': 'H3Africa-test Beacon',
		'address': 'https://beacon2.h3abionet.org/'
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
service_name = 'Services Registry'
service_version = '2.0'
api_version = 'v2.0.0-draft.1'

ga4gh_service_info_group = 'org.ga4gh'
ga4gh_service_info_artifact = 'service-registry'
ga4gh_version = '1.0'

service_types = ['GA4GHRegistry', 'GA4GHBeaconAggregator', 'GA4GHBeacon']

ga4gh_service_types = [
	{
		"group": "org.ga4gh",
		"artifact": "service-registry",
		"version": "1.0.0"
	},
	{
		"group": "org.ga4gh",
		"artifact": "beacon-aggregator",
		"version": "1.0.0"
	},
	{
		"group": "org.ga4gh",
		"artifact": "beacon",
		"version": "1.0.0"
	}
]
