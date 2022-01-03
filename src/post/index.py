import os
import json
import boto3

# Basic class for the WebhookData
# TODO:
# - Add cleaner error handling for when attribtues aren't set
class WebhookData:
    def __init__(self, id, date, type, data):
        self.id = id
        self.date = date
        self.type = type
        self.data = data

# ABOUT THIS LAMBDA FUNCTION:
# Purpose: To persist "webhook data" to a DynamoDB table.
# How: Data should be passed as an object, or a list of objects, in the following format:
# {
#     'id': string || number,
#     'date': string,
#     'type': string,
#     'data': string
# }
# What happens after that:
# Data should be stored (persisted) into the DynamoDB table.
def lambda_handler(event, context):
    # Begin function to persist data...
    try:
        # Load environment variables
        ddbtable = os.environ['ddb_table_id']
        # Instantiate dynamodb client
        dynamodb = boto3.client('dynamodb')
        # Read the body of the request
        body = json.loads(event['body'])
        # Check if the request body contains anything...
        if body:
            # If the body of the request is a list, we need to iterate
            # through each item and use put_item
            if isinstance(body, list):
                # Loop through each object, obtain required information from body of the request...
                for item in body:
                    currentItem = WebhookData(item['id'], item['date'], item['type'], item['data'])
                    # Save
                    dynamodb.put_item(
                        TableName=ddbtable, 
                        Item = {
                            'id':{'N': str(currentItem.id)},
                            'date':{'S': currentItem.date},
                            'type':{'S': currentItem.type},
                            'data':{'S': currentItem.data},
                        }
                    )
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({
                        "Result": "Data successfully saved!"
                    })
                }
            else:
                # Store required information from body of the request...
                currentItem = WebhookData(body['id'], body['date'], body['type'], body['data'])
                # Using body info, save information to the DynamoDB table..
                dynamodb.put_item(
                    TableName=ddbtable, 
                    Item = {
                        'id':{'N': str(currentItem.id)},
                        'date':{'S': currentItem.date},
                        'type':{'S': currentItem.type},
                        'data':{'S': currentItem.data},
                    }
                )
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({
                        "Result": "Data successfully saved!"
                    })
                }
        # Request body was empty, throw an error...
        else:
            print('Error: Request body is empty.')
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "Result": "Error: Request body is empty."
                })
            }
    except Exception as e:
        # If there are any errors...
        print(e)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": e
        }
