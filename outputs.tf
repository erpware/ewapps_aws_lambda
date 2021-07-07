output "api_endpoint" {
  value = aws_api_gateway_stage.ew_app_lambda_stage.invoke_url
}