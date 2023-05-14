# alembic ops

## To create a new file for a new database table in online mode(means project must be running eiher in remote mode(make dev) or local(make devlocal))
> docker-compose exec duro-backend alembic --config app/alembic.ini revision -m "create table_name"
> go to the table created and edit to your choice
> run 'make migrate' this will run the 'make migrate' command in the project makefile

## psql command
> docker ps  
> docker exec -it <container_id> psql -U postgres -d duro_team_beta
> \dt
> 