.DEFAULT_GOAL := help

help: ## Shows this help message
	@printf "\033[1m%s\033[36m %s\033[32m %s\033[0m \n\n" "Development environment for" "pyarr" "";
	@awk 'BEGIN {FS = ":.*##";} /^[a-zA-Z_-]+:.*?##/ { printf " \033[36m make %-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST);
	@echo

requriements: ## Install requirements
	@poetry Install

lint: ## Lint all files
	@isort .
	@python -m black --fast .
	@python -m flake8 pyarr tests
	@python -m mypy pyarr

coverage: ## Check the coverage of the package
	@python -m pytest tests --cov=pyarr --cov-report term-missing -vv
