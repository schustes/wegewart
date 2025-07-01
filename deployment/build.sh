export TF_VAR_repo_url=$ECR_URL/wwapp:v1

cd tf-base
terraform init
terraform plan -out=tfplan
terraform apply -auto-approve

cd ..

aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $ECR_URL
docker build -t wwapp:v1 ..
docker tag wwapp:v1 $TF_VAR_repo_url
docker push $TF_VAR_repo_url

cd tf-app
terraform init
terraform plan -out=tfplan
terraform apply --auto-approve

cd ..
