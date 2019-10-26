import os
import amazondax
import botocore.session

region = os.environ.get('AWS_DEFAULT_REGION', 'us-west-2')

session = botocore.session.get_session()
dynamodb = session.create_client('dynamodb', region_name=region) # low-level client

table_name = "Cart"

params = {
    'TableName' : table_name,
    'KeySchema': [
        { 'AttributeName': "ASIN", 'KeyType' : 'HASH'}   # serial number
    ],
    'AttributeDefinitions': [
        { 'AttributeName': "ASIN", 'AttributeType': "N" }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 10, #can read and write 10 items at a time from dynamo
        'WriteCapacityUnits': 10
    }
}

# Create the table
dynamodb.create_table(**params)

# Wait for the table to exist before exiting
print('Waiting for', table_name, '...')
waiter = dynamodb.get_waiter('table_exists')
waiter.wait(TableName=table_name)
