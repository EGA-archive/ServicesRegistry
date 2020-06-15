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
