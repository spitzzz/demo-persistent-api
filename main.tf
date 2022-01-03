# Create DynamoDB Table
module "persistent-dynamodb-table" {
  source   = "terraform-aws-modules/dynamodb-table/aws"

  name     = "demo-persistent-api-table"
  hash_key = "id"
  server_side_encryption_enabled = true

  attributes = [
    {
      name = "id"
      type = "N"
    }
  ]

  tags = local.tags
}

# Create the lambda function and supporting resources (IAM role, policy(ies), and invoke permissions)
module "lambda-post-persistent-demo" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "demo-persistent-api-post-lambda"
  description   = "Example lambda function that processes POST requests on the Demo Persistent API."
  handler       = "index.lambda_handler"
  runtime       = "python3.8"
  publish       = true
  create_role	  = true
  attach_policies    = true
  policies           = ["arn:aws:iam::aws:policy/AWSXrayReadOnlyAccess"]
  number_of_policies = 1

  attach_policy_statements = true
  policy_statements = {
    dynamodb = {
      effect    = "Allow",
      actions   = ["dynamodb:*"],
      resources = [module.persistent-dynamodb-table.dynamodb_table_arn]
    }
  }

  source_path = "./src/post"

  environment_variables = {
    ddb_table_id = module.persistent-dynamodb-table.dynamodb_table_id
  }

  allowed_triggers = {
    AllowExecutionFromAPIGateway = {
      service    = "apigateway"
      source_arn = "${module.api-demo-persistent.apigatewayv2_api_execution_arn}/*/*"
    }
  }

  tags = local.tags
}

# Create API Gateway related resources
module "api-demo-persistent" {
  source = "terraform-aws-modules/apigateway-v2/aws"

  name          = "demo-persistent-api"
  description   = "Demo Persistent API created using Terraform."
  protocol_type = "HTTP"
  create_api_domain_name = false

  cors_configuration = {
    allow_headers = ["content-type", "x-amz-date", "authorization", "x-api-key", "x-amz-security-token", "x-amz-user-agent"]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }

  # Routes and integrations
  integrations = {
    "POST /" = {
      lambda_arn             = module.lambda-post-persistent-demo.lambda_function_arn
      payload_format_version = "2.0"
      timeout_milliseconds   = 12000
    }

    "$default" = {
      lambda_arn = module.lambda-post-persistent-demo.lambda_function_arn
    }
  }

  tags = local.tags
}
