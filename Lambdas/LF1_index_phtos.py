import json
import boto3
import requests

def detect_labels(photo, bucket):
    labels_res = []

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    print('Detected labels for ' + photo) 
    print()   
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        labels_res.append(label['Name'])
        # print ("Confidence: " + str(label['Confidence']))
        # print ("Instances:")
        # for instance in label['Instances']:
        #     print ("  Bounding box")
        #     print ("    Top: " + str(instance['BoundingBox']['Top']))
        #     print ("    Left: " + str(instance['BoundingBox']['Left']))
        #     print ("    Width: " +  str(instance['BoundingBox']['Width']))
        #     print ("    Height: " +  str(instance['BoundingBox']['Height']))
        #     print ("  Confidence: " + str(instance['Confidence']))
        #     print()

        # print ("Parents:")
        # for parent in label['Parents']:
        #     print ("   " + parent['Name'])
        # print ("----------")
        # print ()
    return labels_res

def lambda_handler(event, context):
    # TODO implement
    print(event)
    bucket = "b2photostore"
    for record in event['Records']:
        image_name = record["s3"]["object"]["key"]
        print(image_name)
        labels_res=detect_labels(image_name, bucket)
        print(labels_res)
        print ("Testing OKAY")
        URL = "https://search-photos-3b5qzqqss44mlqtvgk4f5qy3iy.us-east-1.es.amazonaws.com/photos/_doc"
        header={"Content-Type":"application/json"}
        query={'objectKey':image_name,'bucket':'b2photostore','labels':labels_res}
        response = requests.post(URL, data = json.dumps(query),headers = header)
        dat=json.loads(response.text)
        print (dat)
        # lex = boto3.client('lex-runtime')
        # incoming_msg = "show me cats and dogs"
        # user_id = '111000'
        # bot_name = 'LexSearchBot'
        # response = lex.post_text(
        # botName=bot_name,
        # botAlias=bot_name,
        # userId=user_id,
        # inputText=incoming_msg,
        # )
        # print(response)
        print ("Something")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
