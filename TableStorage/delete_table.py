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

print("Delete a table...")
table_service.delete_table('tasktable')

