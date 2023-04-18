import json
import os

import boto3
from botocore.exceptions import ClientError

dbb = boto3.resource('dynamodb')

def handler(event, context):
  response = {}

  try:
    httpMethod = event.get('httpMethod')
    if not httpMethod or httpMethod != 'GET':
      raise ValueError('Wrong Rest Method')
  
    params = event.get('queryStringParameters') or {}
    user_id = params.get('id')

    if not user_id:
      raise ValueError('Missing user id')

    tableName = os.environ['STORAGE_USERS_NAME']
    table = dbb.Table(tableName)

    response['body'] = json.dumps(get_user(user_id=user_id, table=table))
    response['statusCode'] = 200

  except (Exception, ClientError) as err:
    print(err)
    response['statusCode'] = 400
    response['body'] = { 'error': str(err) }
  
  return response

def get_user(user_id, table):
  user = table.get_item(
    Key={ 'id': user_id },
    ProjectionExpression="firstname, lastname, email, age"
  )

  return { 'user': user.get('Item') }
