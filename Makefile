SHELL := /bin/bash
COMMIT ?= latest

.PHONY: build

all: build

build:
	docker build $(ARGS) \
	       --build-arg REPO=https://github.com/EGA-archive/ServicesRegistry.git \
	       --build-arg COMMIT=$(COMMIT) \
               --build-arg BUILD_DATE="$(shell date +%Y-%m-%d_%H.%M.%S)" \
	       -t cineca/services-registry-test:$(COMMIT) .

up:
	docker run -d --rm \
               --name cineca-services-registry-test \
               -p 5160:8080 \
	       -v $(shell pwd)/tmp/conf.py:/crg/services_registry/conf.py \
               cineca/services-registry-test:$(COMMIT)

down:
	-docker kill cineca-services-registry-test
	-docker rm cineca-services-registry-test

####################################################
# For development

run:
	docker run -d --rm \
               --name cineca-services-registry-test \
               -p 8000:8080 \
	       -v $(shell pwd)/services_registry:/crg/services_registry \
	       -v $(shell pwd)/static:/crg/static \
	       -v $(shell pwd)/templates:/crg/templates \
               --entrypoint "/bin/sleep" \
               cineca/services-registry-test:$(COMMIT) \
           1000000000000


server: CMD=python -m cineca-services-registry-test
exec: CMD=bash
exec server:
	docker exec -it cineca-services-registry-test $(CMD)

####################################################
# Cleaning docker images

define remove_dangling
	docker images $(1) -f "dangling=true" -q | uniq | while read n; do docker rmi -f $$n; done
endef

erase:
	@$(call remove_dangling,cineca/services-registry-test)

purge:
	@$(call remove_dangling,)
