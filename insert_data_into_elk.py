import json
import pandas as pd
from elasticsearch import Elasticsearch
import json

csv_data_file_name = "normalized_data.csv"

db_server_host_addr = "http://localhost"
db_server_port = 9200
db_server_url = db_server_host_addr + ':' + str(db_server_port)

es = Elasticsearch(db_server_url)
print("Estalished a connection to the database server on "+db_server_url)

df = pd.read_csv(csv_data_file_name)
print("Successfuly imported data from the csv file.")

json_data = df.to_json(orient="records", lines=True).splitlines()

print("Trying to index data into db.")

i = 0
failure_counter = 0
for doc in json_data:
    doc = json.loads(doc)
    resp = es.index(index="fiddibo_books", id=i, document=doc)
    retry_counter = 0
    while(resp["_shards"]["successful"] != 1 and retry_counter < 5):
        print("Indexing Data with id=" + str(i) + " failed (" +
              str(retry_counter+1) + "time(s)). Retrying...")
        resp = es.index(index="fiddibo_books", id=i, document=doc)
        retry_counter += 1
    if retry_counter >= 5:
        failure_counter += 1
    i += 1
    if i % 100 == 0:
        print("Successfuly indexed 100 Data records.")

print("Data have been indexed into elk successfuly. Successful="
      + str(i-failure_counter) + " Failed=" + str(failure_counter) + ".")
