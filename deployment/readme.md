# Build script

Executing build.sh creates/updates the complete infrastructure, including docker repo.

## Prerequisites
- Export your docker registry url as var ECR_REGISTRY. AWS ECR registries follow the pattern  "<account_id>.dkr.ecr.<region>.amazonaws.com". E.g. export ECR_REGISTRY = "123456.dkr.ecr.eu-central-1.amazonaws.com"

## Build Steps
- create registry with tf-base
- build and push docker image using shell
- create wwapp lambda, dynamodb table, api-gateway and related resources using tf-app

## Useful hints

- Don't set aws creds env variables, if already present in aws config!
- No login required when using right profile (profile might be necessary to set as variable?)