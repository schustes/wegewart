## Usecase
wegewart is meant to manage reporting requirements for the Schwarzwald Verein - entering routes with some notes and exporting it to an Excel template.

## Technical background
At the same time I wanted to tryout several things:

- Implementing my understanding of Clean Architecture 
- Applying Flask as web framework
- Using AWS services to setup a free infrastructure with AWS ECR, Cognito, Lambda, DynamoDB and S3
- Try out terraform to automate infrastructure and deployment

## Functionality of the app
- Users are managed in the identity provider. Any Oauth2 provider should do.
- On the first login a user entry is created in DynamoDB.
- Then the user can add routes for his tenant.

## Clean architecture
There are 2 modules: Users and Routes. The main structure are these modules. Within each module are the typical hexagonal layers (or rather, circles): adapters, usecases, domain. Dependencies are from the outer to the inner circle, with domain having no dependencies to the outside. Flow of control goes from the outside to the inside and outside (possibly) again. E.g. a show-user web request enters via the controller adapter, calls the user service which in turn calls the UserRepository to load the data. UserRepository is implemented by UserDynamoDBRepository which resides in the outer adpater circle "gateways".

Flask specific files are located in frameworks/flask. Here is also the implementation of the OIDC protocol to authorize users and store them in the database. It takes a shortcut to the UserService directly. It should probably be refactored to reside in the adapters package or provide another controller function there.

## Deploying and running
- It is possible to install a local DynamoDB for testing using the docker-compose.yaml file. For more information, see https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html.
- The app is deployed as docker container using gunicorn. It adds the function wrapper behind the scenes so there is no need for lambda specific code.
- See deployment/readme.md for further details. 

## Prerequisites
- A custom role custom:Verein that identifies the tenant in IAM/Cognito
- A lambda function that maps the custom property to the OIDC token (a "Claims Transformer", see e.g. https://aws.amazon.com/de/blogs/security/how-to-customize-access-tokens-in-amazon-cognito-user-pools/). 
- Also the execution roles of Lambda have to be configured, there is no terraform script for it. It was tedious to find out. In the end I added all dynamodb roles. What is needed:
    - AllowAPIGatewayInvoke for API gateway to forward requests
    - Roles for lambda function to access DynamoDB, S3 and write Cloudwatch logs

## Limitations
- The export function is not available since the template is private information, so there is no template and no S3 terraform. You have to setup yourself.



