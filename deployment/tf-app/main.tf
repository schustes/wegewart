provider "aws" {  
  region = "eu-central-1"
}

variable "repo_url" {
  type = string
}
variable "AUTHORIZE_URL" {
  type    = string
}

variable "CLIENT_ID" {
  type    = string
}

variable "CLIENT_SECRET" {
  type    = string
}

variable "LOGOUT_URL" {
  type    = string
}

variable "LOGOUT_REDIRECT_URL" {
  type    = string
}

variable "REDIRECT_URL" {
  type    = string
}

variable "TOKEN_URL" {
  type    = string
}


resource "aws_dynamodb_table" "users" {
 name = "Users"
 billing_mode = "PAY_PER_REQUEST"
 
 hash_key = "user_id"
 
 attribute {  
   name = "user_id"
   type = "S"  # String data type
 }     

 tags = {
   Name = "Users"
 }
}

resource "aws_dynamodb_table" "routes" {
 name = "Routes"
 billing_mode = "PAY_PER_REQUEST"

 hash_key = "route_id"
 
 attribute {  
   name = "route_id"
   type = "S" 
 }

 attribute {
    name = "date"
    type = "S"
  } 

 global_secondary_index {
    name               = "date-index"
    hash_key           = "date"
    projection_type    = "ALL"
  }  

 tags = {
   Name = "Routes"
 }
}

resource "aws_iam_role" "wwapp_lambda_exec" {
  name = "wwapp_lambda_exec"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

#resource "aws_iam_policy" "lambda_cloudwatch_custom" {
  #name        = "wwapp_lambda_cloudwatch_custom"
  #description = "Custom policy for Lambda to write CloudWatch logs"
  #policy      = jsonencode({
    #Version = "2012-10-17"
    #Statement = [
      #{
        #Effect = "Allow"
        #Action = "logs:CreateLogGroup"
        #Resource = "arn:aws:logs:region:accountID:*"
      #},
      #{
        #Effect = "Allow"
        #Action = [
          #"logs:CreateLogStream",
          #"logs:PutLogEvents"
        #]
        #Resource = [
          #"arn:aws:logs:region:accountID:log-group:/aws/lambda/functionname:*"
        #]
      #}
    #]
  #})
#}

#resource "aws_iam_role_policy_attachment" "logging_access" {
  #role       = aws_iam_role.wwapp_lambda_exec.name
  #policy_arn = aws_iam_policy.lambda_cloudwatch_custom.arn #"arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole"
#}


resource "aws_dynamodb_table" "sessions" {
  name         = "Sessions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }


  ttl {
    attribute_name = "expiration"
    enabled        = true
  }

  tags = {
    Name = "Sessions"
  }
}

resource "aws_iam_role_policy_attachment" "dynamodb_full_access" {
  role       = aws_iam_role.wwapp_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_lambda_function" "wwapp_function" {
  function_name = "wwapp-flask-function"
  package_type  = "Image"
  image_uri     = var.repo_url
  memory_size   = 256
  timeout       = 10
  role          = aws_iam_role.wwapp_lambda_exec.arn
  environment {
    variables = {
      AUTHORIZE_URL       = var.AUTHORIZE_URL
      CLIENT_ID           = var.CLIENT_ID
      CLIENT_SECRET       = var.CLIENT_SECRET
      LOGOUT_REDIRECT_URL = var.LOGOUT_REDIRECT_URL
      REDIRECT_URL        = var.REDIRECT_URL
      TOKEN_URL           = var.TOKEN_URL
    }
  }
}

resource "aws_apigatewayv2_api" "wwapp_api" {
  name          = "wwapp-http-api"
  protocol_type = "HTTP"
}

resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.wwapp_function.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.wwapp_api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_integration" "wwapp_integration" {
  api_id                 = aws_apigatewayv2_api.wwapp_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.wwapp_function.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "wwapp_route" {
  api_id    = aws_apigatewayv2_api.wwapp_api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.wwapp_integration.id}"
}

resource "aws_apigatewayv2_stage" "wwapp_stage" {
  api_id      = aws_apigatewayv2_api.wwapp_api.id
  name        = "$default"
  auto_deploy = true
}

output "wwapp_api_url" {
  description = "API Gateway endpoint URL for wwapp function"
  value       = aws_apigatewayv2_api.wwapp_api.api_endpoint
}

output "wwapp_lambda_arn" {
  description = "wwapp Lambda Function ARN"
  value       = aws_lambda_function.wwapp_function.arn
}

output "wwapp_lambda_role_arn" {
  description = "IAM Role ARN for Flask Lambda"
  value       = aws_iam_role.wwapp_lambda_exec.arn
}
