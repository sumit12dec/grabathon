import boto3
import base64
import json

def lambda_handler(event, context):
    print("event: ", event)
    s3 = boto3.resource('s3')
    bucket = 'facepay-testing-images' #s3.Bucket('facepay-testing-images')
    timestamp = event['timestamp']
    user_id = event['user_id']
    path_test = user_id + '/' + timestamp         # temp path in lambda.
    print("path_test", path_test)
    key = timestamp          # assign filename to 'key' variable
    data = event['img64']             # assign base64 of an image to data variable 
    data1 = data
    img = base64.b64decode(data1)     # decode the encoded image data (base64)
    # with open(path_test, 'w') as data:
    #     data.write(img)
    #     bucket.upload_file(path_test)   # Upload image directly inside bucket
    #     #bucket.upload_file(path_test, 'FOLDERNAME-IN-YOUR-BUCKET /{}'.format(key))    # Upload image inside folder of your s3 bucket.
    rs = s3.Bucket(bucket).put_object(
                Bucket=bucket,
                Key=path_test,
                ContentType='image/jpeg',
                Body=img,
                Metadata = {'x-amz-meta-user-id': user_id}
            )
    
    print('res---------------->',path_test)
    print('key---------------->',key)

    return {
            'status': 'True',
       'statusCode': 200,
       'body': 'Image Uploaded'
      }