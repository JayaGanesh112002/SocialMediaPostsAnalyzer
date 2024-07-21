import json
import boto3
import re

def lambda_handler(event, context):
    # Extracting the post content from event
    msg = event['content']
    
    # Extracting the hashtags. \w matches only alphabets and numbers.
    hashtags = re.findall(r'#\w+', msg)
    
    # Creating a DynamoDB table connection
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Social_Media_Tags'
    table = dynamodb.Table(table_name)
    
    # Getting the real-time record count to generate the next Post's ID
    record_count = table.scan(
        Select = 'COUNT'
        )
    post_id = record_count['Count'] + 1
    
    # Items to be inserted in the DynamoDB table
    item = {
        'Post_ID':int(post_id),
        'Post':msg
    }
    
    # Inserting the post data into table
    try:
        response = table.put_item(Item = item)
    except Exception as e:
        return {
            'statusCode':400,
            'body': json.dumps(f'{e}')
        }

    # Uploading the hashtags to a table
    if len(hashtags)>0:
        try: 
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Hashtags')
            for hashtag in hashtags:
                response = table.update_item(Key={'Hashtag': hashtag},
                UpdateExpression='ADD #Counts:increment',
                ExpressionAttributeNames={'#Counts': 'Counts'},
                ExpressionAttributeValues={':increment': 1})
            return "Posted Successfully."
        except Exception as e:
            return {
                'statusCode':400,
                'body': json.dumps(f'{e}')
            }
    else:
        return "Posted Successfully"