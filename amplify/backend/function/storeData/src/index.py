import os
import boto3
from botocore.exceptions import ClientError

ddb = boto3.resource('dynamodb')

def handler(event, context):
    data_id = event.get('id')
    data = event.get('data')

    try:
        tableName = os.environ['STORAGE_DATA_NAME']
        table = ddb.Table(tableName)

        table.put_item(Item={
            'id': data_id,
            'data': data
        })

        return "OK"

    except (Exception, ClientError) as err:
        print(err)
        return "KO"




