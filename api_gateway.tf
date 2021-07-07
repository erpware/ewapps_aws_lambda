resource "aws_api_gateway_rest_api" "ew_app_lambda" {
  api_key_source           = "HEADER"
  binary_media_types       = []
  description              = "API calls for erpware Lambda Starter."
  minimum_compression_size = -1
  name                     = "ew_app_lambda"

  endpoint_configuration {
    types = [
      "REGIONAL",
    ]
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_deployment" "ew_app_lambda_deployment" {
  rest_api_id = aws_api_gateway_rest_api.ew_app_lambda.id
  lifecycle {
    create_before_destroy = true
  }

  triggers = {
    always_run = data.archive_file.lambda_ew_app_lambda.output_base64sha256
  }
}

resource "aws_api_gateway_stage" "ew_app_lambda_stage" {
  cache_cluster_enabled = false
  deployment_id         = aws_api_gateway_deployment.ew_app_lambda_deployment.id
  rest_api_id           = aws_api_gateway_rest_api.ew_app_lambda.id
  stage_name            = "v1"

  variables            = {}
  xray_tracing_enabled = false
}

resource "aws_api_gateway_integration" "api_ew_app_lambda_integration" {
  cache_key_parameters    = []
  cache_namespace         = aws_api_gateway_rest_api.ew_app_lambda.root_resource_id
  connection_type         = "INTERNET"
  content_handling        = "CONVERT_TO_TEXT"
  http_method             = "POST"
  integration_http_method = "POST"
  passthrough_behavior    = "WHEN_NO_MATCH"
  request_parameters      = {}
  request_templates       = {}
  resource_id             = aws_api_gateway_rest_api.ew_app_lambda.root_resource_id
  rest_api_id             = aws_api_gateway_rest_api.ew_app_lambda.id
  timeout_milliseconds    = 29000
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ew_app_lambda.invoke_arn
}

resource "aws_api_gateway_integration_response" "api_ew_app_lambda_integration_response" {
  http_method = aws_api_gateway_method.api_ew_app_lambda_method.http_method
  resource_id = aws_api_gateway_rest_api.ew_app_lambda.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.ew_app_lambda.id
  status_code = "200"

  depends_on = [
    aws_api_gateway_integration.api_ew_app_lambda_integration
  ]
}

resource "aws_api_gateway_method" "api_ew_app_lambda_method" {
  api_key_required     = false
  authorization        = "NONE"
  authorization_scopes = []
  http_method          = "POST"
  request_models       = {}
  request_parameters   = {}
  resource_id          = aws_api_gateway_rest_api.ew_app_lambda.root_resource_id
  rest_api_id          = aws_api_gateway_rest_api.ew_app_lambda.id
}

