# Build script

Executing build.sh creates/updates the complete infrastructure, including docker repo.

## Prerequisites
- Export your docker registry url as var ECR_URL. AWS ECR registries follow the pattern  "<account_id>.dkr.ecr.<region>.amazonaws.com". E.g. export ECR_URL = "123456.dkr.ecr.eu-central-1.amazonaws.com"
- Export image version IMAGE_VERSION you want to deploy, e.g. export IMAGE_VERSION=v3
- Export your settings for Oauth2 and DynamoDB variables as defined in settings.py

## Build Steps performed in build.sh
- create registry with tf-base
- build and push docker image using shell
- create wwapp lambda, dynamodb table, api-gateway and related resources using tf-app

