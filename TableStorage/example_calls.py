"""
    @version: 20200331.0
    @source: Example taken from https://docs.microsoft.com/en-us/azure/cosmos-db/table-storage-how-to-use-python
"""
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tablebatch import TableBatch
#import socket
import os

the_connection_string = os.getenv('TABLE_CONNECTION_STRING','not_set')

# timeout in seconds
#timeout = 5
#socket.setdefaulttimeout(timeout)

# TableService
# table_service = TableService(account_name='myaccount', account_key='mykey')

# CosmosDB
table_service = TableService(endpoint_suffix="table.cosmos.azure.com", connection_string=the_connection_string)
#table_service.set_proxy("myproxy", 8888)

print("create table...")
table_service.create_table('tasktable')

# dictionary (read from JSON)
print("creating task 001...")
task = {'PartitionKey': 'tasksSeattle', 'RowKey': '001',
        'description': 'Take out the trash', 'priority': 200}
table_service.insert_entity('tasktable', task)

print("Create task through an Entity object...")
task = Entity()
task.PartitionKey = 'tasksSeattle'
task.RowKey = '002'
task.description = 'Wash the car'
task.priority = 100
table_service.insert_entity('tasktable', task)

# update
print("Update task 001...")
task = {'PartitionKey': 'tasksSeattle', 'RowKey': '001',
        'description': 'Take out the garbage', 'priority': 250}
table_service.update_entity('tasktable', task)

# Replace the entity created earlier
print("Replace task using insert_or_replace... - Take out the garbage again")
task = {'PartitionKey': 'tasksSeattle', 'RowKey': '001',
        'description': 'Take out the garbage again', 'priority': 250}
table_service.insert_or_replace_entity('tasktable', task)

# Insert a new entity
print("insert or replay rowkey 003 - buy detergent")
task = {'PartitionKey': 'tasksSeattle', 'RowKey': '003',
        'description': 'Buy detergent', 'priority': 300}
table_service.insert_or_replace_entity('tasktable', task)

# batch processing - Add multiple entries
print("batch processing task 004/005")
batch = TableBatch()
task004 = {'PartitionKey': 'tasksSeattle', 'RowKey': '004',
           'description': 'Go grocery shopping', 'priority': 400}
task005 = {'PartitionKey': 'tasksSeattle', 'RowKey': '005',
           'description': 'Clean the bathroom', 'priority': 100}
batch.insert_entity(task004)
batch.insert_entity(task005)
table_service.commit_batch('tasktable', batch)

# alternative way to use batch, using context
print("batch insert using context...")
task006 = {'PartitionKey': 'tasksSeattle', 'RowKey': '006',
           'description': 'Go grocery shopping', 'priority': 400}
task007 = {'PartitionKey': 'tasksSeattle', 'RowKey': '007', 'newCol': 'newColVal1',
           'description': 'Clean the bathroom', 'priority': 100}

with table_service.batch('tasktable') as batch:
    batch.insert_entity(task006)
    batch.insert_entity(task007)

# Query
print("Query task 001...")
task = table_service.get_entity('tasktable', 'tasksSeattle', '001')
print(task.description)
print(task.priority)

# Query a set of entities
print("Query set of entities...")
tasks = table_service.query_entities(
    'tasktable', filter="PartitionKey eq 'tasksSeattle'")
for task in tasks:
    print(task.description)
    print(task.priority)
    try:
       print(task.newCol)
    except AttributeError:
       print("No newCol.")

# Query a subset of entity properties
print("Query a subset of entity properties...")
tasks = table_service.query_entities(
    'tasktable', filter="PartitionKey eq 'tasksSeattle'", select='description')
for task in tasks:
    print(task.description)

# Delete an entity
print("Delete an entity...")
table_service.delete_entity('tasktable', 'tasksSeattle', '001')

# Delete a table
print("Delete a table...")
table_service.delete_table('tasktable')

