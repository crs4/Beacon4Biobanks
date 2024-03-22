SHELL := /bin/bash
#.PHONY: build run exec down server

all: test-with-molgenis test-no-molgenis down

up:
	docker-compose up -d
down-molgenis:
	docker-compose stop molgenis
down:
	docker-compose down -v
test-with-molgenis: up
	docker-compose exec beacon pytest tests/integration/molgenis -m molgenis_up
test-no-molgenis: up down-molgenis
	docker-compose exec beacon pytest tests/integration/molgenis -m molgenis_down
