help: ## show help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## build the project
	docker-compose build

up-daemon: ## start the project at background
	docker-compose up -d

up: ## start the project
	docker-compose up

down: ## delete all conatainers and volumes
	docker-compose down -v

stop: ## stop the project
	docker-compose stop

shell-web: ## connect to the web container
	docker-compose exec web /bin/bash

tests: ## run tests
	docker-compose exec web /bin/bash -c "poetry run pytest -v"
