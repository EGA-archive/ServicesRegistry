SHELL := /bin/bash
COMMIT ?= latest

.PHONY: build

all: build

build:
	docker build $(ARGS) \
	       --build-arg REPO=https://github.com/EGA-archive/ServicesRegistry.git \
	       --build-arg COMMIT=$(COMMIT) \
               --build-arg BUILD_DATE="$(shell date +%Y-%m-%d_%H.%M.%S)" \
	       -t crg/services-registry:$(COMMIT) .

up:
	docker run -d --rm \
               --name services-registry \
               -p 8000:8000 \
               crg/services-registry:$(COMMIT)

down:
	-docker kill services-registry
	-docker rm services-registry

####################################################
# For development

run:
	docker run -d --rm \
               --name services-registry \
               -p 8000:8000 \
	       -v $(shell pwd)/services_registry:/crg/services_registry \
	       -v $(shell pwd)/static:/crg/static \
               --entrypoint "/bin/sleep" \
               crg/services-registry:$(COMMIT) \
           1000000000000


server: CMD=python -m services_registry
exec: CMD=bash
exec server:
	docker exec -it services-registry $(CMD)

####################################################
# Cleaning docker images

define remove_dangling
	docker images $(1) -f "dangling=true" -q | uniq | while read n; do docker rmi -f $$n; done
endef

erase:
	@$(call remove_dangling,crg/services-registry)

purge:
	@$(call remove_dangling,)
