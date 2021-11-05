host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = {
	# 'ca.distributedgenomics.poc': {
	# 	'name': 'PseudoCHILD Beacon',
	# 	'address': 'https://poc.distributedgenomics.ca:5061/api'
	# },
	# 'heg-beacon': {
	# 	'name': 'heg Beacon',
	# 	'address': 'https://beacon.text-analytics.ch/api'
	# },
	'org.ega-archive.beacon-giab-demo': {
		'name': 'EGA Beacon - Genome In A Bottle',
		'address': 'https://beacon-giab-demo.ega-archive.org/api',
		'order': '1',
		'verifier': 'org.ega-archive.beacon-giab-demo.json'
	},
	'org.progenetix.beacon': {
		'name': 'Progenetix Cancer Genomics Beacon+',
		'address': 'https://progenetix.org/beacon/info',
		'order': '2',
		'verifier': 'org.progenetix.beacon.json'
	},
	'org.rd-connect.beacon': {
		'name': 'Beacon @ RD-Connect',
		'address': 'https://playground.rd-connect.eu/beacon2/api',
		'order': '3',
		'verifier': 'org.rd-connect.beacon.json'
	},
	'uk.ac.le.lamp.www448': {
		'name': 'CafeVariome beacon',
		'address': 'https://www448.lamp.le.ac.uk/beacon/BeaconApi/info',
		'order': '4',
		'verifier': ''
	},
	'org.cafevariome.beaconv2': {
		'name': 'Cafe Variome Beacon v2',
		'address': 'https://beaconv2.cafevariome.org',
		'order': '5',
		'verifier': ''
	}
	# 'org.ega-archive.beacon': {
	# 	'name': 'Beacon Test Instance',
	# 	'address': 'https://beacon-giab-test.ega-archive.org/api'
	# }
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
service_title = 'Beacon v2 GA4GH Approval Registry'
service_logos = [
	{
		'href': 'https://ega-archive.org',
		'img': 'https://static.ega-archive.org/img/logo.png',
		'title': 'EGA European Genome-Phenome Archive'
	},
	{
		'href': 'https://crg.eu',
		'img': 'https://static.ega-archive.org/img/CRG_blue.jpg',
		'title': 'Centre for Genomic Regulation'
	}
]

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

default_logo = '/static/img/no_logo.png'
