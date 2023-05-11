stop:
	docker-compose down --remove-orphans

start: stop
	docker-compose up --build

dev: stop
	STAGE=dev docker-compose up --build

devlocal: stoplocal
	STAGE=dev docker-compose -f docker-compose-with-local-db.yml up --build

devtest:
	docker-compose exec authentifyer-backend pytest -s -v app/tests/${TEST_FILE}

migrate:
	docker-compose exec authentifyer-backend alembic --config app/alembic.ini upgrade head

rollback:
	docker-compose exec authentifyer-backend alembic --config app/alembic.ini downgrade -1

rollback-all:
	docker-compose exec authentifyer-backend alembic --config app/alembic.ini downgrade base
