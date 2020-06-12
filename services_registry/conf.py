host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = [ ('EGA Beacon v0.3', 'https://ega-archive.org/beacon-api/'),
			#('EGA Beacon', 'https://beacon-api.ega-archive.org'),
			 ('Covid Beacon', 'https://covid19beacon.crg.eu/api/')]

# either whitelist or blacklist should be provided
urls_whitelisted = ['^\/$',
					'^\/service-info$',
					'^\/query\?[\/a-zA-Z0-9]*',
					'^\/g_variants[\/a-zA-Z0-9]*',
					'^\/biosamples[\/a-zA-Z0-9]*',]

urls_blacklisted = []
# urls_blacklisted = ['^\/individuals[\/a-zA-Z0-9]*']
