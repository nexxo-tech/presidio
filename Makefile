.PHONY: build

build:
	@echo "Building..."
	@docker build ./presidio-analyzer -t nexxo/presidio-analyzer:latest -t sortify.azurecr.io/presidio-analyzer:latest

push:
	@echo "Pushing..."
	@docker push sortify.azurecr.io/presidio-analyzer:latest