.PHONY: build

VERSION = 1.0.0

build:
	@echo "Building..."
	@docker build ./presidio-analyzer -f ./presidio-analyzer/Dockerfile -t sortify.azurecr.io/presidio-analyzer:latest -t sortify.azurecr.io/presidio-analyzer:$(VERSION)

build-transformers:
	@echo "Building..."
	@docker build ./presidio-analyzer -f ./presidio-analyzer/Dockerfile.transformers -t sortify.azurecr.io/presidio-analyzer:transformers

push:
	@echo "Pushing..."
	@docker push sortify.azurecr.io/presidio-analyzer:latest
	@docker push sortify.azurecr.io/presidio-analyzer:$(VERSION)