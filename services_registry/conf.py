host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = {
	'ca.distributedgenomics.poc.beaconv2': {
		'name': 'PseudoCHILD Beacon',
		'address': 'https://poc.distributedgenomics.ca:5061/api'
	},
	'h3abionet-test-beacon': {
		'name': 'H3Africa-test Beacon',
		'address': 'https://beacon2.h3abionet.org/api'
	},
	'heg-beacon': {
		'name': 'heg Beacon',
		'address': 'https://beacon.text-analytics.ch/api'
	},
	'ega-beacon': {
		'name': 'EGA Beacon - Genome In A Bottle',
		'address': 'https://beacon-giab-test.ega-archive.org/api'
	},
}

urls_whitelisted = [r'^/api/.*'] # anything after /api

# urls_whitelisted = [r'^/$',
# 		    r'^/query?.*',
# 		    r'^/genomic_snp?.*',
# 		    r'^/genomic_region?.*',
# 		    r'^/g_variants.*',
# 		    r'^/biosamples.*',
# 		    r'^/datasets',
# 		    r'^/cohorts']

urls_blacklisted = []

# Service Registry info
service_id = 'eu.crg.services-registry'
service_name = 'CRG Services Registry'
service_version = '1.0'
api_version = 'v2.0.0-draft.1'

# Elixir
elixir_service_type_group = 'org.elixir-europe'
elixir_service_type_artifact = 'service-registry'
# elixir_service_type_version = api_version

service_types = ['org.elixir-europe.service-registry',
				 'org.elixir-europe.beacon-aggregator',
				 'org.elixir-europe.beacon']

# GA4GH
ga4gh_service_type_group = 'org.ga4gh'
ga4gh_service_type_artifact = 'service-registry'
ga4gh_service_type_version = '1.0'

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
