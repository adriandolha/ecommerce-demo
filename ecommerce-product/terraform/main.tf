terraform {
  backend "s3" {
    # s3 should be terraform-state-$accountid/$client/$component
    bucket         = "terraform-state-103050589342"
    key            = "products"
    region         = "us-east-1"
  }
}


# define a policy for the iam role
resource "aws_iam_policy" "policy_iam_for_lambda" {
  name        = "policy_iam_for_lambda_"
  description = "A policy to manage lambda/ec2 access for iam_for_lambda"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "*",
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
EOF
}
# attach the above policy to the role
resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = "${aws_iam_policy.policy_iam_for_lambda.arn}"
}


resource "aws_dynamodb_table" "products_dynamo_table" {
  name = "products"
  read_capacity = 5
  write_capacity = 5
  hash_key = "product_id"


  attribute {
    name = "product_id"
    type = "S"
  }

  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        },
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

resource "aws_iam_role_policy" "ddb_policy" {
  name = "ddb_policy"
  role = "${aws_iam_role.iam_for_lambda.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
            "Effect": "Allow",
            "Action": [
                "dynamodb:*"
            ],
            "Resource": "arn:aws:dynamodb:${var.region}:${var.accountId}:table/*"
        }
  ]
}
EOF
}

resource "aws_iam_role_policy" "basic_execution_policy" {
  name = "basic_policy"
  role = "${aws_iam_role.iam_for_lambda.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
              "sqs:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        },
        {
            "Action": [
              "logs:CreateLogGroup",
              "logs:CreateLogStream",
              "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*",
            "Effect": "Allow"
      },
      {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
      }
    ]
}
EOF
}

resource "aws_lambda_function" "list_product_lambda" {
  filename = "${pathexpand("lambda_package_ecommerce_product.zip")}"
  function_name = "products_list"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "aws.list"
  source_code_hash = "${base64sha256(file(pathexpand("lambda_package_ecommerce_product.zip")))}"
  runtime = "python3.6"
  timeout = 15
}



resource "aws_api_gateway_rest_api" "product_api" {
  name = "product_api"
  description = "Product API"
  endpoint_configuration {
    types = [
      "REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "products_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.product_api.id}"
  parent_id = "${aws_api_gateway_rest_api.product_api.root_resource_id}"
  path_part = "products"
}

resource "aws_api_gateway_method" "list_products" {
  rest_api_id = "${aws_api_gateway_rest_api.product_api.id}"
  resource_id = "${aws_api_gateway_resource.products_resource.id}"
  http_method = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "product_api_integration_list" {
  rest_api_id = "${aws_api_gateway_rest_api.product_api.id}"
  resource_id = "${aws_api_gateway_resource.products_resource.id}"
  http_method = "${aws_api_gateway_method.list_products.http_method}"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "${aws_lambda_function.list_product_lambda.invoke_arn}"

}

resource "aws_api_gateway_deployment" "product_api_deployment" {
  depends_on = [
    "aws_api_gateway_integration.product_api_integration_list"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.product_api.id}"
  stage_name = "test"
}


resource "aws_lambda_permission" "apigw_lambda_permission_add" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.list_product_lambda.arn}"
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.product_api.execution_arn}/*/*/*"
}