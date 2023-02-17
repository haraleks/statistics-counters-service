PROJECT_NAME ?= Stat service
VERSION = $(shell python3.9 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= haraleks
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

all:

	@echo "make run                              - Create & run development environment in terminal (realtime)"
	@echo "make clean                            - Clean docker volumes"
	@echo "make stop                             - Stops docker containers and delete them"
	@echo "make clean_images                     - Clean docker images"
	@echo "make test                             - Test all"
	@echo "make migrate                          - Make migrate db"
	@exit 0

_clean_makefile:
	rm -fr *.egg-info dist

_down_docker:
	docker-compose down --remove-orphans

clean:
	docker volume prune

run:
	docker-compose -f docker-compose.yml up --build

build:
	docker-compose -f docker-compose.yml up -d --build

test: start_test_docker stop

stop: _down_docker _clean_makefile

clean_images:
	docker image prune -a -f

start_test_docker:
	docker-compose run --rm -e DB_NAME=stat_test app_stat pytest -vvv sc_service/tests/ -x

migrate:
	docker-compose run --rm app_stat bash -c "cd sc_service && alembic upgrade head"