terraform {
  backend "s3" {
    # s3 should be terraform-state-$accountid/$client/$component
    bucket = "terraform-state-103050589342"
    key = "shoppingcarts"
    region = "us-east-1"
  }
}


resource "aws_dynamodb_table" "shoppingcarts_dynamo_table" {
  name = "shoppingcarts"
  read_capacity = 5
  write_capacity = 5
  hash_key = "user_id"


  attribute {
    name = "user_id"
    type = "S"
  }

  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
}


resource "aws_lambda_function" "list_shoppingcart_lambda" {
  filename = "${pathexpand("lambda_package.zip")}"
  function_name = "shoppingcarts_list"
  role = "arn:aws:iam::103050589342:role/iam_for_lambda"
  handler = "aws.list"
  source_code_hash = "${base64sha256(file(pathexpand("lambda_package.zip")))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_lambda_function" "add_shoppingcart_lambda" {
  filename = "${pathexpand("lambda_package.zip")}"
  function_name = "shoppingcarts_add"
  role = "arn:aws:iam::103050589342:role/iam_for_lambda"
  handler = "aws.add"
  source_code_hash = "${base64sha256(file(pathexpand("lambda_package.zip")))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_api_gateway_rest_api" "shoppingcart_api" {
  name = "shoppingcart_api"
  description = "ShoppingCart API"
  endpoint_configuration {
    types = [
      "REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "shoppingcarts_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.shoppingcart_api.id}"
  parent_id = "${aws_api_gateway_rest_api.shoppingcart_api.root_resource_id}"
  path_part = "shoppingcarts"
}

resource "aws_api_gateway_method" "list_shoppingcarts" {
  rest_api_id = "${aws_api_gateway_rest_api.shoppingcart_api.id}"
  resource_id = "${aws_api_gateway_resource.shoppingcarts_resource.id}"
  http_method = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "add_shoppingcarts" {
  rest_api_id = "${aws_api_gateway_rest_api.shoppingcart_api.id}"
  resource_id = "${aws_api_gateway_resource.shoppingcarts_resource.id}"
  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "shoppingcart_api_integration_list" {
  rest_api_id = "${aws_api_gateway_rest_api.shoppingcart_api.id}"
  resource_id = "${aws_api_gateway_resource.shoppingcarts_resource.id}"
  http_method = "${aws_api_gateway_method.list_shoppingcarts.http_method}"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "${aws_lambda_function.list_shoppingcart_lambda.invoke_arn}"

}

resource "aws_api_gateway_integration" "shoppingcart_api_integration_add" {
  rest_api_id = "${aws_api_gateway_rest_api.shoppingcart_api.id}"
  resource_id = "${aws_api_gateway_resource.shoppingcarts_resource.id}"
  http_method = "${aws_api_gateway_method.add_shoppingcarts.http_method}"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "${aws_lambda_function.add_shoppingcart_lambda.invoke_arn}"

}

resource "aws_api_gateway_deployment" "shoppingcart_api_deployment" {
  depends_on = [
    "aws_api_gateway_integration.shoppingcart_api_integration_list"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.shoppingcart_api.id}"
  stage_name = "test"
}


resource "aws_lambda_permission" "apigw_lambda_permission_list" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.list_shoppingcart_lambda.arn}"
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.shoppingcart_api.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "apigw_lambda_permission_add" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.add_shoppingcart_lambda.arn}"
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.shoppingcart_api.execution_arn}/*/*/*"
}