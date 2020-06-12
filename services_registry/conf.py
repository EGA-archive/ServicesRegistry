host = '0.0.0.0'
port = 8000

# import ssl
ssl_context = None

services = [ ('EGA Beacon v0.3', 'https://ega-archive.org/beacon-api/'),
			#('EGA Beacon', 'https://beacon-api.ega-archive.org'),
			 ('Covid Beacon', 'https://covid19beacon.crg.eu/api/')]

# services = ['https://service-1.domain.tld',
# 	      'https://service-2.domain.tld']

urls = []