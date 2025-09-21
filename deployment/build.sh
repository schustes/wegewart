export TF_VAR_repo_url=$ECR_URL/wwapp:$IMAGE_VERSION

export TF_VAR_CLIENT_ID=$CLIENT_ID #cognito app client id
export TF_VAR_CLIENT_SECRET=$CLIENT_SECRET #cognito app client secret
export TF_VAR_TOKEN_URL=$TOKEN_URL #cognito token url
export TF_VAR_AUTHORIZE_URL=$AUTHORIZE_URL #cognito authorize url
export TF_VAR_LOGOUT_URL=$LOGOUT_URL  #cognito logout url  
export TF_VAR_USER_URL=$USER_URL #cognito user info url
export TF_VAR_REDIRECT_URL=$REDIRECT_URL #app redirect url after login (e.g. https://pip8dl4cc0.execute-api.eu-central-1.amazonaws.com/index)
export TF_VAR_LOGOUT_REDIRECT_URL=$LOGOUT_REDIRECT_URL #app redirect url after logout (e.g. https://pip8dl4cc0.execute-api.eu-central-1.amazonaws.com/index)

echo $TF_VAR_repo_url

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
