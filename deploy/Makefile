all: down up load reindex rebuild

up:
	docker-compose up -d beacon

rebuild:
	docker-compose rm -sf beacon && \
	docker-compose build beacon && \
	docker-compose up -d beacon && \
	docker-compose logs -f beacon

logs:
	docker-compose logs -f beacon

relaunch:
	docker-compose up beacon

down:
	docker-compose down

verify:
	beacon-verifier http://localhost:5050/api/

# only works with justfile (https://github.com/casey/just#recipe-parameters)
test COLLECTION REQUEST:
	http POST http://localhost:5050/api/{{COLLECTION}}/ --json < {{REQUEST}}
