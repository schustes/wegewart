provider "aws" {  
  region = "eu-central-1"
}

variable "repo_url" {
  type = string
}

resource "aws_dynamodb_table" "users" {
 name = "UsersTable"
 billing_mode = "PROVISIONED"
 read_capacity = 10
 write_capacity = 5

 hash_key = "UserId"
 
 attribute {  
   name = "UserId"
   type = "S"  # String data type
 }     

 tags = {
   Name = "UsersTable"
 }
}

resource "aws_dynamodb_table_item" "item" {
  table_name = aws_dynamodb_table.users.name
  hash_key   = aws_dynamodb_table.users.hash_key

  item = <<ITEM
{
   "UserId": {"S": "a8954662-6115-4c64-819c-19f68a46cee6"},
   "name": {"S": "Stephan"},
   "email": {"S": "info@stephan-schuster.net"}
}
ITEM
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
