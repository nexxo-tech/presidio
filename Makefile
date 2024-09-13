.PHONY: build

build:
	@echo "Building..."
	@docker build ./presidio-analyzer -f ./presidio-analyzer/Dockerfile -t sortify.azurecr.io/presidio-analyzer:latest

build-transformers:
	@echo "Building..."
	@docker build ./presidio-analyzer -f ./presidio-analyzer/Dockerfile.transformers -t sortify.azurecr.io/presidio-analyzer:transformers

push:
	@echo "Pushing..."
	@docker push sortify.azurecr.io/presidio-analyzer:latest
	@docker push sortify.azurecr.io/presidio-analyzer:transformers