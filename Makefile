include .env
export

help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<command>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } ' $(MAKEFILE_LIST)
.PHONY: help

compose-up-prod:
	docker-compose up -d --build && docker-compose logs -f
.PHONY: compose-up-prod

compose-down:
	docker-compose down
.PHONY: compose-up-prod

linter-check:
	flake8 .
.PHONY: lint
