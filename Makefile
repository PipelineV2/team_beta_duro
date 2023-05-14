dependencies:
	@pip-compile requirements.in -o requirements.txt
	@pip-compile requirements.in requirements-dev.in -o requirements-dev.txt
	pip-sync requirements-dev.txt

stop:
	docker-compose down --remove-orphans

start: stop
	docker-compose up --build

dev: stop
	STAGE=dev docker-compose up --build
	
stoplocal:
	docker-compose -f docker-compose-with-local-db.yml down --remove-orphans

devlocal: stoplocal
	STAGE=dev docker-compose -f docker-compose-with-local-db.yml up --build

devtest:
	docker-compose exec duro-backend pytest -s -v app/tests/${TEST_FILE}

migrate:
	docker-compose exec duro-backend alembic --config app/alembic.ini upgrade head

rollback:
	docker-compose exec duro-backend alembic --config app/alembic.ini downgrade -1

rollback-all:
	docker-compose exec duro-backend alembic --config app/alembic.ini downgrade base
