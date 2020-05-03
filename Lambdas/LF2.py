import json
import boto3
import requests

def lambda_handler(event, context):
    # TODO implement
    print(event['search_query'])
    print(context)
    lex = boto3.client('lex-runtime')
    incoming_msg = event['search_query']
    user_id = '111000'
    bot_name = 'LexSearchBot'
    response = lex.post_text(
        botName=bot_name,
        botAlias=bot_name,
        userId=user_id,
        inputText=incoming_msg,
    )
    print(response)
    keyword_two=None
    search=""
    keyword_one=response["slots"]["keyword_one"]
    search=search+keyword_one
    if ("keyword_two" in response["slots"] and response["slots"]["keyword_two"]):
        keyword_two=response["slots"]["keyword_two"]
        search=search+" "+keyword_two
    print (keyword_one)
    #print (keyword_two)
    print (search)
    URL = "https://search-photos-3b5qzqqss44mlqtvgk4f5qy3iy.us-east-1.es.amazonaws.com/photos/_search"
    header={"Content-Type":"application/json"}
    query = {"size":1000 ,"query": {"match": {"labels":search}}}
    response = requests.post(URL, data = json.dumps(query),headers = header)
    #response=requests.get(URL)
    dat=json.loads(response.text)
    print (dat)
    es=dat["hits"]["hits"]
    res=[]
    for i in es:
        res.append(i["_source"]["objectKey"])
    print (res)
    return {
        'statusCode': 200,
        'body': json.dumps({"files":res})
    }
