# Services Registry (SR)
Registry for dispatching HTTP requests to a fixed list of services.

## Server

### Configuration

The main configuration file is located at: `services_registry/conf.py`

It contains the following:
* list of services registered in this SR as a Python dictionary. 

    It uses the service Id as the key and contains the service name and URL:
```python
services = {
    'ega-beacon': {
        'name': 'EGA Beacon',
        'address': 'https://ega-archive.org/beacon-api'
    },
}
```
  
* list of URLs whitelisted and/or blacklisted:
```python
urls_whitelisted = [r'^/$',
		    r'^/query?.*',
		    r'^/genomic_snp?.*',
		    r'^/genomic_region?.*',
		    r'^/g_variants.*',
		    r'^/biosamples.*',
		    r'^/datasets',
		    r'^/cohorts']

urls_blacklisted = []
```
Note that if `urls_whitelisted` is empty, any URL will be accepted.

* information about the SR and service types supported:
```python
# Service Registry info
service_id = 'eu.crg.services-registry'
service_name = 'CRG Services Registry'
service_version = '1.0'
api_version = 'v2.0.0-draft.1'

# Elixir
elixir_service_type_group = 'org.elixir-europe'
elixir_service_type_artifact = 'service-registry'

service_types = ['org.elixir-europe.service-registry', 
				 'org.elixir-europe.beacon-aggregator', 
				 'org.elixir-europe.beacon']
```

* information about the SR for GA4GH compatible endpoints:
```python
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
```

## Deployment

### Docker

```shell script

```

TODO: 
* How to inject the config file
* How to deploy the server
* How to deploy the UI

### Server development

The SR is deployed in port `8000` by default. To change it, edit the variable called `port` in `conf.py`. You can also change the host with variable `host`. 

Run the following commands to start the server:
```shell script
make build
make run
make server
```
After changing some code, kill it and start it again running `make server`.

### UI development

The UI is deployed in port `TODO` by default. 

TODO

## API endpoints

#### Service info
* http://localhost:8000/info
* http://localhost:8000/bn_service_types
* http://localhost:8000/bn_services

#### Requesting alternative schemas
* http://localhost:8000/info?requestedSchemasServiceInfo=ga4gh-service-info-v1.0
* http://localhost:8000/bn_services?requestedSchemasServiceInfo=ga4gh-service-info-v1.0

#### GA4GH Service-info compatible
* http://localhost:8000/service-info
* http://localhost:8000/info?model=ga4gh-service-info-v1.0 
* http://localhost:8000/services/types
* http://localhost:8000/services
* http://localhost:8000/bn_services?model=ga4gh-service-info-v1.0

#### Call forwarding

Any other value written after `http://localhost:8000` will be automatically forwarded to all the registered services, as long as it is a whitelisted value and it is not blacklisted.

* http://localhost:8000/cohorts
* http://localhost:8000/datasets
* http://localhost:8000/query?assemblyId=GRCh37&referenceName=Y&start=2655470&referenceBases=A&alternateBases=C
* http://localhost:8000/genomic_snp?assemblyId=GRCh37&referenceName=Y&start=2655470&referenceBases=A&alternateBases=C
* http://localhost:8000/genomic_region?referenceName=Y&assemblyId=GRCh37&start=2655470&end=2655472
* http://localhost:8000/g_variants?referenceName=Y&start=2655470&referenceBases=A&alternateBases=C
* http://localhost:8000/g_variants/240763
* http://localhost:8000/biosamples?start=272&end=273
* http://localhost:8000/biosamples/SRS6508490