import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Hashtags'
    table = dynamodb.Table(table_name)
    response = table.scan()
    response = response['Items']
    sorted_response = sorted(response,
    key = lambda x:x['Counts'],
    reverse = True)
    return sorted_response