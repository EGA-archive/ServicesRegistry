SHELL := /bin/bash
COMMIT ?= latest

SERVICE=crg-services-registry
IMG=crg/services-registry:$(COMMIT)

CONTAINER_PORT=18080

.PHONY: build

all: build

build:
	docker build $(ARGS) \
	       --build-arg REPO=https://github.com/EGA-archive/ServicesRegistry.git \
	       --build-arg COMMIT=$(COMMIT) \
               --build-arg BUILD_DATE="$(shell date +%Y-%m-%d_%H.%M.%S)" \
	       -t $(IMG) .

up:
	docker run -d --rm \
               --name "$(SERVICE)" \
               -p $(CONTAINER_PORT):8080 \
	       -v $(shell pwd)/services_registry:/crg/services_registry \
	       -v $(shell pwd)/static:/crg/static \
	       -v $(shell pwd)/templates:/crg/templates \
               $(IMG)

down:
	-docker stop "$(SERVICE)"
	-docker rm "$(SERVICE)"

ps:
	docker ps | grep '$(SERVICE)'

wait:
	@sleep 3
reboot: down wait up

####################################################
# For development

run: ENTRYPOINT=--entrypoint "/bin/sleep"
run: CMD=365d
run:
	docker run -d --rm \
               --name $(SERVICE) \
               -p 8000:8000 \
               -p 8001:8001 \
               -p $(CONTAINER_PORT):8080 \
	       -v $(shell pwd)/services_registry:/crg/services_registry \
	       -v $(shell pwd)/static:/crg/static \
	       -v $(shell pwd)/templates:/crg/templates \
               $(ENTRYPOINT) $(IMG) $(CMD)


server: CMD=python -m services_registry
exec: CMD=bash
exec server:
	docker exec -it $(SERVICE) $(CMD)
