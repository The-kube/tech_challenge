# tech_challenge
Sources:

https://blog.stoplight.io/python-rest-api
http://exploreflask.com/en/latest/storing.html
https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04
https://hub.docker.com/_/postgres
https://stackoverflow.com/questions/35069027/docker-wait-for-postgresql-to-be-running

Start up the DB
docker compose up -d flask_db

Access the DB and check data
docker exec -it <your-postgres-container-id> bash
psql -d postgres -U postgres
select * from users;

Build Docker Image
docker compose build

Start Docker containers in background 
docker compose up -d flask_api 


Debug docker image
docker run -it --entrypoint /bin/bash <IMAGE_NAME> -s
docker run -it --entrypoint /bin/bash corradot/flask_api_app:1.0.0 -s