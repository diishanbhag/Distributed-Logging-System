from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
filterer_consumer = KafkaConsumer(
    'all_logs',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
ELASTIC_INDEX = 'logs'

for message in filterer_consumer:
    log_entry = message.value
    try:
        log_message = json.loads(log_entry['message'].replace("'", "\"")) 
    except Exception as e:
        log_message = log_entry
        
    message_type = log_message.get('message_type')
    if message_type == 'HEARTBEAT':           
        continue
    es.index(index=ELASTIC_INDEX, body=log_entry)
    print(f"Indexed log entry to Elasticsearch: {log_entry}")
