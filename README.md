# ewapps_aws_lambda

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=P9PSQ7LZNTNB4)

This repository contains the backend for the ewapps_aws_lambda, which provides an AWS API Gateway to list, and invoke other AWS Lambda functions.

We will provide some clients

* Windows https://www.erpware.de/tools/ewapps_aws_lambda/
* Android https://play.google.com/store/apps/details?id=co.erpware.ewapps_aws_lambda

## setup - with terraform

Download or clone this repository and adjust the variable for the security token.
Run **terraform init** to download all necessary providers. After completion, run **terraform apply**. If you encouter any error of missing resources, run it a second time.

This will create an AWS API Gateway and integrates the Lambda function to it.

The output parameter will give you the generated URL of the API Gateway.

## setup - manually

We prefer using terraform, but ok, some of you want to create it manually or will integrate it in existing services:

* Create AWS Lambda function and upload the code from lambda_function.py
* Adjust the policy of the IAM User to be able to list and invoke lambda functions.
* Integrate the AWS Lambda to an API Gateway. 

## How it works

We provide three actions, which you have to send as POST request to the API Gateway. Each request need the securitystring, you added as environment variable to the AWS Lambda.

### status
With this request, you will receive a list of all AWS Lambda functions.

### invoke
The invoke request just invokes a Lambda function based on the ARN, you provide during the request. The request will wait until the Lamba is finished or API Gateway timeout (29sec).

# erpware

ewapps_aws_lambda is one of the tools, we are using within our company "erpware" (https://www.erpware.de (german) / https://www.erpware.co (english)). Apps for Android (possible later for iOS). Most of our tools are freeware or waiting for a small donation.
