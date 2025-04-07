from kafka import KafkaConsumer
import json

# Initialize the KafkaConsumer
consumer = KafkaConsumer(
    'critical_logs',
    'node_failure',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

# Process each message
for message in consumer:
    data = message.value 
    log_type = data.get('message_type', 'unknown')  
    status=data.get('status','unknown')
    if log_type == 'REGISTRATION' and status =='UP':
        print("🌟 Registration Successful: A new node has been registered.")
    elif log_type =='REGISTRATION' and status =='DOWN':
        print("⚠️ Alert: A node's heartbeat has stopped.")
    else:
        print("❌ Error Alert: An error occurred in your application!")

