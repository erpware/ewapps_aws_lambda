import json
import os

import boto3
from botocore import exceptions

lambdaclient = boto3.client('lambda')
lambdaclientinvoke = boto3.client('lambda')

# Responses
# 200:  Request was executed successful
# 400:  No action or invalid action requested
# 401:  Secure String not send
# 403:  Secure String does not match
# 412:  Secure String is not set in environment variables
# 417:  Missing RDS Instances IDs to fulfill the action
# 500:  Errors during execution of specific actions
# 502:  Bad request -> mostly an configuration issue of API Gateway


def lambda_handler(event, context):
    # do all necessary pre checks
    # 1. is the environment variable set?
    try:
        securestring = os.environ['SECURESTRING']
    except KeyError:
        return {
            'statusCode': 412,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Environment variable SECURESTRING not set.'
            })
        }
    # 2. is the securestring send by your request
    if 'body' in event:
        body = json.loads(event['body'])
        if 'securestring' not in body:
            return {
                'statusCode': 401,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'Necessary secure token not provided by your request.'
                })
            }
        # 3. does the securestring match the environment variable
        if not (body['securestring'] == securestring):
            return {
                'statusCode': 403,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'You are not allowed to execute this function.'
                })
            }
        # now, everything is fine, let's do our action
        if 'action' in body:
            action = body['action']
            if action == 'status':
                return get_all_functions()
            if action == 'invoke':
                if 'lambdaarn' not in body:
                    return {
                        'statusCode': 417,
                        'headers': {
                            'Content-Type': 'application/json'
                        },
                        'body': json.dumps({
                            'message': 'Necessary Lambda function name not provided by your request.'
                        })
                    }
                return invoke_function(body['lambdaarn'])

    return {
        'statusCode': 400,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'No action or an invalid action send. Nothing to do.'
        })
    }


def get_all_functions():
    functions = []
    # get all instances
    for lambdafunction in lambdaclient.list_functions()['Functions']:
        print(lambdafunction)
        function = {
            'lambdaarn': lambdafunction['FunctionArn'],
            'runtime': lambdafunction['Runtime'],
            'name': lambdafunction['FunctionName']
        }
        functions.append(function)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'functions': functions
        })
    }


def invoke_function(lambdaarn):
    try:
        response = lambdaclientinvoke.invoke(
            FunctionName=lambdaarn,
            InvocationType='RequestResponse'
        )
        payload = response['Payload'].read().decode()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Function {0} successfully invoked'.format(lambdaarn),
                'response': payload
            }, indent=2)
        }
    except exceptions.ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': repr(e)
            })
        }
