from __future__ import print_function

import boto3
from decimal import Decimal
import json

print('Loading function')

def create_collection(collection_id):

    client = boto3.client('rekognition')

    #Create a collection
    print('Creating collection:' + collection_id)
    response = client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')


# --------------- Helper Functions ------------------

def index_faces(bucket, key, collection_id):
    try:
        response = rekognition.index_faces(
            Image={"S3Object":
                {"Bucket": bucket,
                "Name": key}},
                CollectionId=collection_id)
    except Exception as e:
        print(str(e))
        print("Collection Not found.")
        create_collection(collection_id)
        response = rekognition.index_faces(
            Image={"S3Object":
                {"Bucket": bucket,
                "Name": key}},
                CollectionId=collection_id)
    return response
    
def update_index(tableName, faceId, user_id):
    print("hello1")
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'face_id': {'S': faceId},
            'user_id': {'S': user_id}
            }
        ) 
    print("Done adding to table")
    
# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("here", event)
    # print("here1", json.loads(event))
    
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(bucket, key)
    # bucket = event['bucket']
    # key = event['collection_id']
    # collection_id = event['collection_id']

    try:

        # Calls Amazon Rekognition IndexFaces API to detect faces in S3 object 
        # to index faces into specified collection
        ret = s3.head_object(Bucket=bucket, Key=key)
        print("ret", ret)
        user_id = ret['Metadata']['x-amz-meta-user-id']        
        collection_id = user_id
        
        response = index_faces(bucket, key, collection_id)
        
        # Commit faceId and full name object metadata to DynamoDB
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            update_index("facepay", faceId, user_id)

        # Print response to console
        print(response)
        return {'face_id': faceId, 'user_id': user_id}
    except Exception as e:
        print(str(e))

# def create_collection(event, context):

#     client = boto3.client('rekognition')

#     #Create a collection
#     collection_id = event['collection_id']
#     print('Creating collection:' + collection_id)
#     response = client.create_collection(CollectionId=collection_id)
#     print('Collection ARN: ' + response['CollectionArn'])
#     print('Status code: ' + str(response['StatusCode']))
#     print('Done...')
#     return {'collection_arn': response['CollectionArn']}
    