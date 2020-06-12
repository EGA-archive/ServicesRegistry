host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = [ ('EGA Beacon v0.3', 'https://ega-archive.org/beacon-api/'),
			#('EGA Beacon', 'https://beacon-api.ega-archive.org'),
			 ('Covid Beacon', 'https://covid19beacon.crg.eu/api/')]


urls_whitelisted = ['^\/$',
					'^\/service-info$',
					'^\/query\?.*',
					'^\/g_variants.*',
					'^\/biosamples.*',]

urls_blacklisted = []
