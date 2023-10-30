.PHONY: build

build:
	@echo "Building..."
	@docker build ./presidio-analyzer -t nexxo/presidio-analyser:latest