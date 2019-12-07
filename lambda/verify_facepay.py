import boto3
import io
import base64
# from PIL import Image

rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# image = Image.open("group1.jpeg")
# stream = io.BytesIO()
# image.save(stream,format="JPEG")
# image_binary = stream.getvalue()

def lambda_handler(event, context):
    user_id = event['user_id']
    base64_image = event['image']
    base_64_binary = base64.b64decode(base64_image)

    response = rekognition.search_faces_by_image(
            CollectionId=user_id,
            Image = {'Bytes': base_64_binary}                                       
            )
    # print("response", response)
    for match in response['FaceMatches']:
        print(match['Face']['FaceId'], match['Face']['Confidence'])
            
        face = dynamodb.get_item(
            TableName='facepay',  
            Key={'face_id': {'S': match['Face']['FaceId']}}
            )
        if 'Item' in face:
            return {"user_id": face['Item']['user_id']['S'],
                    "confidence": match['Face']['Confidence'],
                    "message": "User authenticated successfully"}
    
    return {"user_id": user_id, "confidence": 0, "message": "User couldn't be authenticated"}