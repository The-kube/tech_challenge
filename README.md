# tech_challenge
## Flask API app with access to Postgres DB
Simple implementation of a flask API server that access a Postgres DB store user data, routes:
 - POST /user
 - GET  /users

Check more on *requests.http *

### TODO:
 - Avoid storing AWS access keys in plain text
 - Stateful set for DB instance for scale-up
 - Variabilize more Helm Values
 - Automatize/script more the entire process
 - Freeze pip requirements.txt
 - Improve AWS Terraform IAM roles, credentials
 - Integrate Ingress into helm deploy
## Requirements
- awscli, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
- kubectl
-  terraform
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/users
get AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXX
get AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXX
```
## Usage
configure AWS credentials
```
aws configure
```
Create EKS cluster and configure kubectl
```
cd terraform
terraform init
terraform apply
aws eks update-kubeconfig --region "eu-north-1" --name "cluster-apiapp-eks"
```
We should now have kubectl configured for the EKS cluster, let's deploy the helm conf:
```
cd helm
pwd
...path/tech_challenge/terraform/helm

terraform init
terraform apply
```
Check resources
```
kubectl get pod,svc,ing
```
We can now deploy Ingress conf and check Ingress adress
```
kubectl apply -f ../../ingress/deploy.yaml

kubectl get ing

NAME                 CLASS   HOSTS              ADDRESS                                                                          PORTS   AGE
apiapp-api-ingress   nginx   corradoapiapp.io   a925040944d294d5584d40fd9f78b946-2d225911ab5932af.elb.eu-north-1.amazonaws.com   80      2m32s
```
Use this address in /etc/hosts, IP creation may take some time
```
ping a925040944d294d5584d40fd9f78b946-2d225911ab5932af.elb.eu-north-1.amazonaws.com

echo "51.21.30.98 corradoapiapp.io" | sudo tee -a  /etc/hosts
```
You can now send requests to "corradoapiapp.io" endpoint like:
```
GET USERS:
curl http://corradoapiapp.io/users

INSERT USER:
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"bob john","email":"bobjohn@mil.com"}' \
  http://corradoapiapp.io/user

GET RUNNING NODE
curl http://corradoapiapp.io/details

GET USER BY ID
curl http://corradoapiapp.io/users/1

DELETE USER
curl http://corradoapiapp.io/user/3 --request DELETE

UPDATE USER BY ID
curl --header "Content-Type: application/json" \
  --request PUT \
  --data '{"username":"jack john","email":"jackjohn@mil.com"}' \
  http://corradoapiapp.io/user/4
```
# Uninstall
Note: Ingress delete may take some time
```
kubectl delete -f ../../ingress/deploy.yaml
pwd
..../tech_challenge/terraform/helm
terraform destroy
cd ..
terraform destroy
remove /etc/hosts reference
```
# Commands and troubleshooting
### Start up the DB locally on docker
```
docker compose up -d flask_db
```
### Access the DB and check data
```
docker exec -it <your-postgres-container-id> bash
psql -d postgres -U postgres
select * from users;
```
### Build Docker Image
```
docker compose build
```
### Start Docker containers in background 
```
docker compose up -d flask_api 
```
### Debug docker image
```
docker run -it --entrypoint /bin/bash <IMAGE_NAME> -s
docker run -it --entrypoint /bin/bash thekube/flask_api_app:1.0.0 -s
```
### Kubectl get shell
```
kubectl exec --stdin --tty <pod> -- /bin/bash
```
### Convert docker image into mainfests files and apply
```
kompose convert
kubectl apply -f flask-db-claim0-persistentvolumeclaim.yaml,flask-db-deployment.yaml,flask-db-service.yaml,flask-api-deployment.yaml,flask-api-service.yaml
```

### Convert manifest files into helm chart using helmify
```
cd kubernetes; awk 'FNR==1 && NR!=1  {print "---"}{print}' *.yaml | helmify flapp
```

### Terraform
```
cd terraform
terraform init
terraform apply

aws eks update-kubeconfig --region "eu-north-1" --name "cluster-apiapp-eks"
```

### Deploy ingress
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml
kubectl get pods -n ingress-nginx
```
### Tools used to test
 - REST Client extension for VSCode to test the API
>https://marketplace.visualstudio.com/items?itemName=humao.rest-client
 - DBeaver to test DB
 - Minikube to test k8s locally
 - Kompose to convert docker image into mainfests files
 >https://github.com/kubernetes/kompose/
 - Helmify to convert manifest files into helm release
 >https://github.com/arttor/helmify
### Sources:
>https://blog.stoplight.io/python-rest-api
>
>http://exploreflask.com/en/latest/storing.html
>
>https://hub.docker.com/_/postgres
>
>https://github.com/hashicorp/learn-terraform-provision-eks-cluster/
>
>https://developer.hashicorp.com/terraform/tutorials/kubernetes/eks
>
>https://github.com/arttor/helmify
>
>https://kubernetes.github.io/ingress-nginx/deploy/#aws
