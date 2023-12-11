# tech_challenge
Sources:

https://blog.stoplight.io/python-rest-api
http://exploreflask.com/en/latest/storing.html
https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04
https://hub.docker.com/_/postgres
https://stackoverflow.com/questions/35069027/docker-wait-for-postgresql-to-be-running
https://github.com/hashicorp/learn-terraform-provision-eks-cluster/
https://developer.hashicorp.com/terraform/tutorials/kubernetes/eks
https://github.com/arttor/helmify

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

Kubectl get shell
kubectl exec --stdin --tty <pod> -- /bin/bash

Convert docker image into deployment and apply
kompose convert
kubectl apply -f flask-db-claim0-persistentvolumeclaim.yaml,flask-db-deployment.yaml,flask-db-service.yaml,flask-api-deployment.yaml,flask-api-service.yaml

Convert manifest files into helm chart using helmify
cd kubernetes; awk 'FNR==1 && NR!=1  {print "---"}{print}' *.yaml | helmify flapp
