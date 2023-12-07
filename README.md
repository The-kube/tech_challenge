# tech_challenge
Sources:

https://blog.stoplight.io/python-rest-api
http://exploreflask.com/en/latest/storing.html
https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04
https://hub.docker.com/_/postgres
https://medium.com/codex/how-to-persist-and-backup-data-of-a-postgresql-docker-container-9fe269ff4334
https://stackoverflow.com/questions/35069027/docker-wait-for-postgresql-to-be-running

Start up the DB
docker compose up -d flask_db

Access the DB and check data
docker exec -it <your-postgres-container-id> bash
psql -d postgres -U postgres
select * from users;

Debug docker image
docker run -it --entrypoint /bin/bash <IMAGE_NAME> -s
docker run -it --entrypoint /bin/bash corradot/flask_api_app:1.0.0 -s